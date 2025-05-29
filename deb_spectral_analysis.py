#!/usr/bin/env python3
"""
Dimensional Entanglement Bottleneck (DEB) Theory - Spectral Flow Analysis
Complete implementation of the 4-node minimal model with spectral analysis
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

class DEBSystem:
    """4-node Dimensional Entanglement Bottleneck system"""
    
    def __init__(self, alpha0=0.5, beta0=0.3, E0=0.8, lambda1=0.1, lambda2=1.0, 
                 tau_c=5.0, sigma=2.0):
        self.alpha0 = alpha0
        self.beta0 = beta0
        self.E0 = E0
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.tau_c = tau_c
        self.sigma = sigma
        
    def bottleneck_function(self, tau):
        """Sigmoid bottleneck activation function"""
        return 0.5 * (1 + np.tanh(self.sigma * (tau - self.tau_c)))
    
    def entanglement_tensor(self, state):
        """Calculate total entanglement from state vector"""
        alpha1, alpha2, alpha3, alpha4, beta1, beta2 = state
        return (alpha1 * alpha2 * alpha3 * alpha4 + 
                beta1 * beta2 + 
                alpha1 * alpha3 * beta1 + 
                alpha2 * alpha4 * beta2)
    
    def derivatives(self, tau, state):
        """Evolution equations for the 4-node system"""
        alpha1, alpha2, alpha3, alpha4, beta1, beta2 = state
        
        # Current entanglement
        E_current = self.entanglement_tensor(state)
        
        # Bottleneck activation
        f_bottle = self.bottleneck_function(tau)
        
        # Calculate derivatives
        entanglement_error = E_current - self.E0
        
        dalpha1_dt = (-2 * entanglement_error * (alpha2*alpha3*alpha4 + alpha3*beta1) - 
                      2 * self.lambda2 * f_bottle * alpha1)
        dalpha2_dt = (-2 * entanglement_error * (alpha1*alpha3*alpha4 + alpha4*beta2) - 
                      2 * self.lambda2 * f_bottle * alpha2)
        dalpha3_dt = (-2 * entanglement_error * (alpha1*alpha2*alpha4 + alpha1*beta1) - 
                      2 * self.lambda2 * f_bottle * alpha3)
        dalpha4_dt = (-2 * entanglement_error * (alpha1*alpha2*alpha3 + alpha2*beta2) - 
                      2 * self.lambda2 * f_bottle * alpha4)
        dbeta1_dt = (-2 * entanglement_error * (beta2 + alpha1*alpha3) - 
                     2 * self.lambda1 * beta1)
        dbeta2_dt = (-2 * entanglement_error * (beta1 + alpha2*alpha4) - 
                     2 * self.lambda1 * beta2)
        
        return [dalpha1_dt, dalpha2_dt, dalpha3_dt, dalpha4_dt, dbeta1_dt, dbeta2_dt]
    
    def evolve(self, tau_max=10.0, num_points=1000):
        """Evolve the system from tau=0 to tau_max"""
        initial_state = [self.alpha0, self.alpha0, self.alpha0, self.alpha0, 
                        self.beta0, self.beta0]
        tau_span = (0, tau_max)
        tau_eval = np.linspace(0, tau_max, num_points)
        
        solution = solve_ivp(self.derivatives, tau_span, initial_state, 
                           t_eval=tau_eval, method='RK45', rtol=1e-8)
        
        return solution

class SpectralAnalyzer:
    """Spectral analysis tools for DEB system"""
    
    @staticmethod
    def build_transfer_matrix(state):
        """
        Construct entanglement transfer matrix from 4-node state.
        Nodes arranged in square: n1-n2
                                  |  |
                                  n4-n3
        """
        alpha1, alpha2, alpha3, alpha4, beta1, beta2 = state
        
        # 4x4 correlation matrix
        T = np.zeros((4, 4))
        
        # Edge correlations (square topology)
        T[0,1] = T[1,0] = abs(alpha1)  # n1-n2
        T[1,2] = T[2,1] = abs(alpha2)  # n2-n3
        T[2,3] = T[3,2] = abs(alpha3)  # n3-n4
        T[3,0] = T[0,3] = abs(alpha4)  # n4-n1
        
        # Diagonal correlations
        T[0,2] = T[2,0] = abs(beta1)   # n1-n3
        T[1,3] = T[3,1] = abs(beta2)   # n2-n4
        
        # Self-correlations (diagonal = 1)
        np.fill_diagonal(T, 1.0)
        
        return T
    
    @staticmethod
    def analyze_spectral_evolution(solution):
        """Compute eigenvalue evolution throughout the simulation"""
        eigenvalue_trajectory = []
        spectral_gaps = []
        
        for i in range(solution.y.shape[1]):
            state = solution.y[:, i]
            T = SpectralAnalyzer.build_transfer_matrix(state)
            
            # Eigenvalues in descending order
            eigvals = np.linalg.eigvalsh(T)
            eigvals = np.sort(eigvals)[::-1]
            
            # Spectral gap between largest two eigenvalues
            gap = eigvals[0] - eigvals[1] if len(eigvals) > 1 else 0
            
            eigenvalue_trajectory.append(eigvals)
            spectral_gaps.append(gap)
        
        return {
            'eigenvalues': np.array(eigenvalue_trajectory),
            'spectral_gaps': np.array(spectral_gaps),
            'tau_range': solution.t
        }
    
    @staticmethod
    def identify_geometric_modes(transfer_matrix):
        """
        Identify eigenmodes that correspond to geometric (distance-like) patterns
        """
        eigvals, eigvecs = np.linalg.eigh(transfer_matrix)
        
        # Sort by eigenvalue magnitude
        idx = np.argsort(eigvals)[::-1]
        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]
        
        geometric_scores = []
        for i, eigvec in enumerate(eigvecs.T):
            # Test if eigenvector reflects square geometry
            # Neighbors should be more correlated than diagonals
            
            # Neighboring correlations: (0,1), (1,2), (2,3), (3,0)
            neighbor_corr = np.mean([
                abs(eigvec[0] * eigvec[1]),  # n1-n2
                abs(eigvec[1] * eigvec[2]),  # n2-n3
                abs(eigvec[2] * eigvec[3]),  # n3-n4
                abs(eigvec[3] * eigvec[0])   # n4-n1
            ])
            
            # Diagonal correlations: (0,2), (1,3)
            diagonal_corr = np.mean([
                abs(eigvec[0] * eigvec[2]),  # n1-n3
                abs(eigvec[1] * eigvec[3])   # n2-n4
            ])
            
            # Geometric score: preference for neighbors over diagonals
            if diagonal_corr > 0:
                geometric_score = neighbor_corr / diagonal_corr
            else:
                geometric_score = neighbor_corr
                
            geometric_scores.append(geometric_score)
        
        return eigvals, eigvecs, geometric_scores

class CriticalAnalysis:
    """Critical point and scaling analysis"""
    
    @staticmethod
    def power_law(x, a, b, x0):
        """Power law function: a * |x - x0|^b"""
        return a * np.abs(x - x0)**b
    
    @staticmethod
    def extract_critical_exponents(spectral_data, tau_c, window=1.0):
        """
        Extract critical exponents by fitting power laws near tau_c
        """
        tau = spectral_data['tau_range']
        gaps = spectral_data['spectral_gaps']
        
        # Focus on region near critical point
        mask = np.abs(tau - tau_c) < window
        tau_critical = tau[mask]
        gaps_critical = gaps[mask]
        
        # Remove points where gap is zero
        nonzero_mask = gaps_critical > 1e-10
        tau_fit = tau_critical[nonzero_mask]
        gaps_fit = gaps_critical[nonzero_mask]
        
        if len(tau_fit) < 5:
            return None
        
        try:
            # Fit: gap ~ |tau - tau_c|^(z*nu)
            popt, pcov = curve_fit(
                lambda t, a, b: CriticalAnalysis.power_law(t, a, b, tau_c),
                tau_fit, gaps_fit,
                p0=[1.0, 0.5],
                bounds=([0.1, 0.1], [10.0, 3.0])
            )
            
            amplitude, exponent = popt
            amplitude_err, exponent_err = np.sqrt(np.diag(pcov))
            
            return {
                'critical_exponent': exponent,
                'amplitude': amplitude,
                'exponent_error': exponent_err,
                'amplitude_error': amplitude_err,
                'r_squared': CriticalAnalysis.calculate_r_squared(
                    gaps_fit, 
                    CriticalAnalysis.power_law(tau_fit, amplitude, exponent, tau_c)
                )
            }
        except:
            return None
    
    @staticmethod
    def calculate_r_squared(y_true, y_pred):
        """Calculate R-squared goodness of fit"""
        ss_tot = np.sum((y_true - np.mean(y_true))**2)
        ss_res = np.sum((y_true - y_pred)**2)
        return 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

class DEBVisualizer:
    """Visualization tools for DEB analysis"""
    
    @staticmethod
    def plot_parameter_evolution(solution, system):
        """Plot evolution of alpha and beta parameters"""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))
        
        # Parameter evolution
        ax1.plot(solution.t, solution.y[0], 'b-', label='α₁', linewidth=2)
        ax1.plot(solution.t, solution.y[1], 'b--', label='α₂', alpha=0.7)
        ax1.plot(solution.t, solution.y[2], 'b:', label='α₃', alpha=0.7)
        ax1.plot(solution.t, solution.y[3], 'b-.', label='α₄', alpha=0.7)
        ax1.axvline(system.tau_c, color='red', linestyle='--', alpha=0.5, label='τc')
        ax1.set_ylabel('Edge Parameters (α)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_title('DEB Parameter Evolution')
        
        ax2.plot(solution.t, solution.y[4], 'g-', label='β₁', linewidth=2)
        ax2.plot(solution.t, solution.y[5], 'g--', label='β₂', linewidth=2)
        ax2.axvline(system.tau_c, color='red', linestyle='--', alpha=0.5, label='τc')
        ax2.set_ylabel('Diagonal Parameters (β)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Entanglement conservation
        entanglement_history = [system.entanglement_tensor(solution.y[:, i]) 
                              for i in range(len(solution.t))]
        ax3.plot(solution.t, entanglement_history, 'purple', linewidth=2, label='Total Entanglement E')
        ax3.axhline(system.E0, color='orange', linestyle='--', label=f'Target E₀={system.E0}')
        ax3.axvline(system.tau_c, color='red', linestyle='--', alpha=0.5, label='τc')
        ax3.set_xlabel('τ')
        ax3.set_ylabel('Entanglement E')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_spectral_evolution(spectral_data, tau_c):
        """Plot eigenvalue evolution through bottleneck"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        
        # All eigenvalues
        eigenvalues = spectral_data['eigenvalues']
        tau_range = spectral_data['tau_range']
        
        colors = ['red', 'blue', 'green', 'orange']
        for i in range(eigenvalues.shape[1]):
            ax1.plot(tau_range, eigenvalues[:, i], color=colors[i], 
                    linewidth=2, label=f'λ_{i+1}')
        
        ax1.axvline(tau_c, color='black', linestyle='--', alpha=0.7, label='τc (bottleneck)')
        ax1.set_ylabel('Eigenvalues λᵢ(τ)')
        ax1.set_title('Spectral Flow Through Dimensional Bottleneck')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Spectral gap
        ax2.plot(tau_range, spectral_data['spectral_gaps'], 'purple', 
                linewidth=2, label='Spectral Gap Δ = λ₁ - λ₂')
        ax2.axvline(tau_c, color='black', linestyle='--', alpha=0.7, label='τc')
        ax2.set_xlabel('τ')
        ax2.set_ylabel('Spectral Gap Δ(τ)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_critical_scaling(spectral_data, critical_fit, tau_c):
        """Plot critical scaling behavior"""
        if critical_fit is None:
            print("No critical fit available")
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        tau = spectral_data['tau_range']
        gaps = spectral_data['spectral_gaps']
        
        # Linear scale
        ax1.plot(tau, gaps, 'b-', alpha=0.7, label='Spectral Gap Data')
        
        # Plot fit
        tau_fit = np.linspace(tau_c - 2, tau_c + 2, 200)
        gap_fit = CriticalAnalysis.power_law(tau_fit, 
                                           critical_fit['amplitude'],
                                           critical_fit['critical_exponent'],
                                           tau_c)
        ax1.plot(tau_fit, gap_fit, 'r--', linewidth=2, 
                label=f"Fit: Δ ∼ |τ-τc|^{critical_fit['critical_exponent']:.2f}")
        ax1.axvline(tau_c, color='black', linestyle='--', alpha=0.5)
        ax1.set_xlabel('τ')
        ax1.set_ylabel('Spectral Gap Δ')
        ax1.set_title('Critical Scaling (Linear)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Log-log scale
        mask = (np.abs(tau - tau_c) > 0.1) & (gaps > 1e-6)
        if np.sum(mask) > 0:
            ax2.loglog(np.abs(tau[mask] - tau_c), gaps[mask], 'bo', alpha=0.7, 
                      label='Data')
            
            tau_log = np.logspace(-1, 1, 50)
            gap_log = critical_fit['amplitude'] * tau_log**critical_fit['critical_exponent']
            ax2.loglog(tau_log, gap_log, 'r--', linewidth=2, 
                      label=f"Slope = {critical_fit['critical_exponent']:.2f}")
            
        ax2.set_xlabel('|τ - τc|')
        ax2.set_ylabel('Spectral Gap Δ')
        ax2.set_title('Critical Scaling (Log-Log)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def run_complete_deb_analysis():
    """
    Run complete DEB analysis: evolution + spectral analysis + critical scaling
    """
    print("🔥 Starting Complete DEB Analysis 🔥")
    print("="*50)
    
    # Initialize system
    system = DEBSystem(
        alpha0=0.8,    # Strong initial edge entanglement
        beta0=0.3,     # Moderate diagonal entanglement
        E0=1.5,        # Target total entanglement
        lambda1=0.5,   # Locality penalty
        lambda2=2.0,   # Bottleneck strength
        tau_c=5.0,     # Bottleneck center
        sigma=1.0      # Bottleneck sharpness
    )
    
    print(f"System parameters:")
    print(f"  Initial state: α₀={system.alpha0}, β₀={system.beta0}")
    print(f"  Target entanglement: E₀={system.E0}")
    print(f"  Penalties: λ₁={system.lambda1}, λ₂={system.lambda2}")
    print(f"  Bottleneck: τc={system.tau_c}, σ={system.sigma}")
    print()
    
    # Evolve system
    print("🧮 Evolving system...")
    solution = system.evolve(tau_max=10.0, num_points=1000)
    print(f"✅ Evolution completed: {len(solution.t)} time points")
    
    # Spectral analysis
    print("🔬 Analyzing spectral evolution...")
    spectral_data = SpectralAnalyzer.analyze_spectral_evolution(solution)
    print(f"✅ Spectral analysis completed")
    
    # Critical point analysis
    print("📊 Extracting critical exponents...")
    critical_fit = CriticalAnalysis.extract_critical_exponents(
        spectral_data, system.tau_c, window=1.5
    )
    
    if critical_fit:
        print(f"✅ Critical analysis completed:")
        print(f"  Critical exponent: {critical_fit['critical_exponent']:.3f} ± {critical_fit['exponent_error']:.3f}")
        print(f"  R² goodness of fit: {critical_fit['r_squared']:.3f}")
    else:
        print("⚠️  Critical analysis failed - insufficient data near critical point")
    
    # Geometric mode analysis
    print("🔍 Analyzing geometric modes...")
    final_state = solution.y[:, -1]
    final_transfer_matrix = SpectralAnalyzer.build_transfer_matrix(final_state)
    eigvals, eigvecs, geometric_scores = SpectralAnalyzer.identify_geometric_modes(
        final_transfer_matrix
    )
    
    print(f"✅ Geometric analysis completed:")
    print(f"  Final eigenvalues: {eigvals}")
    print(f"  Geometric scores: {geometric_scores}")
    
    # Visualization
    print("📈 Generating visualizations...")
    DEBVisualizer.plot_parameter_evolution(solution, system)
    DEBVisualizer.plot_spectral_evolution(spectral_data, system.tau_c)
    if critical_fit:
        DEBVisualizer.plot_critical_scaling(spectral_data, critical_fit, system.tau_c)
    
    # Summary
    print("\n" + "="*50)
    print("🎯 ANALYSIS SUMMARY")
    print("="*50)
    
    initial_E = system.entanglement_tensor([system.alpha0] * 4 + [system.beta0] * 2)
    final_E = system.entanglement_tensor(final_state)
    
    print(f"Entanglement conservation:")
    print(f"  Initial: {initial_E:.3f}")
    print(f"  Final: {final_E:.3f}")
    print(f"  Target: {system.E0:.3f}")
    print(f"  Error: {abs(final_E - system.E0):.3f}")
    
    print(f"\nParameter evolution:")
    print(f"  Initial α: {system.alpha0:.3f} → Final α: {final_state[:4].mean():.3f}")
    print(f"  Initial β: {system.beta0:.3f} → Final β: {final_state[4:].mean():.3f}")
    
    if critical_fit:
        print(f"\nCritical behavior:")
        print(f"  Critical exponent: {critical_fit['critical_exponent']:.3f}")
        print(f"  Expected range: 0.5-2.0 (mean-field to Ising)")
        
    print(f"\nGeometric emergence:")
    dominant_mode = np.argmax(geometric_scores)
    print(f"  Dominant geometric mode: {dominant_mode + 1}")
    print(f"  Geometric score: {geometric_scores[dominant_mode]:.3f}")
    
    return {
        'system': system,
        'solution': solution,
        'spectral_data': spectral_data,
        'critical_fit': critical_fit,
        'geometric_analysis': (eigvals, eigvecs, geometric_scores)
    }

if __name__ == "__main__":
    # Run the complete analysis
    results = run_complete_deb_analysis()
    
    print("\n🚀 Analysis complete! The universe has condensed from entanglement to geometry! 🚀")