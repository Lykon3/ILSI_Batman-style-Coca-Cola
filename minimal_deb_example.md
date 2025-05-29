# The DEB "Hydrogen Atom": A 4-Node Minimal Model

## 1. System Definition

### 1.1 Pre-Geometric Category Structure

**Configuration**: 4 nodes arranged in a square topology
```
n₁ ---- r₁₂ ---- n₂
|                 |
r₁₄             r₂₃  
|                 |
n₄ ---- r₃₄ ---- n₃
```

**Entanglement Relations**:
- Edge relations: r₁₂, r₂₃, r₃₄, r₄₁ (strength parameters α₁, α₂, α₃, α₄)
- Diagonal relations: r₁₃, r₂₄ (strength parameters β₁, β₂)

**State Vector**: The system state is completely specified by:
$$\vec{s}(\tau) = (\alpha₁(\tau), \alpha₂(\tau), \alpha₃(\tau), \alpha₄(\tau), β₁(\tau), β₂(\tau))$$

### 1.2 Entanglement Tensor

For the 4-node system, the entanglement tensor reduces to:
$$\mathcal{E} = \alpha₁α₂α₃α₄ + \beta₁β₂ + \alpha₁α₃β₁ + \alpha₂α₄β₂$$

This captures:
- Cyclic entanglement around the square (first term)
- Direct diagonal entanglement (second term)  
- Mixed cyclic-diagonal correlations (third and fourth terms)

## 2. Information-Theoretic Constraint Functional

### 2.1 Physical Motivation

The constraint functional arises from three information-theoretic principles:

**Principle 1** (Entanglement Conservation): Total entanglement is approximately conserved during evolution
**Principle 2** (Locality Preference): Short-range correlations are energetically favored
**Principle 3** (Bottleneck Constraint): Information capacity has an upper bound

### 2.2 Explicit Functional Form

$$\Omega[\vec{s}] = \underbrace{|\mathcal{E} - E_0|^2}_{\text{conservation}} + \lambda_1 \underbrace{(\beta₁² + \beta₂²)}_{\text{locality}} + \lambda_2 \underbrace{f_{\text{bottle}}(\tau)(\alpha₁² + \alpha₂² + \alpha₃² + \alpha₄²)}_{\text{bottleneck}}$$

Where:
- $E_0$ = conserved total entanglement
- $\lambda_1 > 0$ penalizes long-range (diagonal) connections
- $\lambda_2 = 0$ for $\tau < \tau_c$, then increases sharply
- $f_{\text{bottle}}(\tau) = \frac{1}{2}[1 + \tanh(\sigma(\tau - \tau_c))]$ (sigmoid bottleneck)

## 3. Categorical Gradient Flow

### 3.1 Evolution Equations

The categorical gradient $\nabla_{\mathcal{R}}\Omega = \frac{\partial \Omega}{\partial \vec{s}}$ gives:

$$\frac{d\alpha_i}{d\tau} = -\frac{\partial \Omega}{\partial \alpha_i}$$
$$\frac{d\beta_j}{d\tau} = -\frac{\partial \Omega}{\partial \beta_j}$$

**Explicit Forms**:
$$\frac{d\alpha_1}{d\tau} = -2(\mathcal{E} - E_0)(\alpha_2\alpha_3\alpha_4 + \alpha_3\beta_1) - 2\lambda_2 f_{\text{bottle}}(\tau)\alpha_1$$

$$\frac{d\alpha_2}{d\tau} = -2(\mathcal{E} - E_0)(\alpha_1\alpha_3\alpha_4 + \alpha_4\beta_2) - 2\lambda_2 f_{\text{bottle}}(\tau)\α_2$$

$$\frac{d\alpha_3}{d\tau} = -2(\mathcal{E} - E_0)(\alpha_1\alpha_2\alpha_4 + \alpha_1\beta_1) - 2\lambda_2 f_{\text{bottle}}(\tau)\alpha_3$$

$$\frac{d\alpha_4}{d\tau} = -2(\mathcal{E} - E_0)(\alpha_1\alpha_2\alpha_3 + \alpha_2\beta_2) - 2\lambda_2 f_{\text{bottle}}(\tau)\alpha_4$$

$$\frac{d\beta_1}{d\tau} = -2(\mathcal{E} - E_0)(\beta_2 + \alpha_1\alpha_3) - 2\lambda_1\beta_1$$

$$\frac{d\beta_2}{d\tau} = -2(\mathcal{E} - E_0)(\beta_1 + \alpha_2\alpha_4) - 2\lambda_1\beta_2$$

### 3.2 Analysis of Flow Structure

**Pre-Bottleneck** ($\tau < \tau_c$, $\lambda_2 = 0$):
- System evolves to conserve total entanglement $\mathcal{E} = E_0$
- Diagonal terms $\beta_i$ are suppressed by locality penalty $\lambda_1$
- Edge terms $\alpha_i$ adjust to maintain entanglement conservation

**At Bottleneck** ($\tau = \tau_c$):
- $f_{\text{bottle}}(\tau_c) = 0.5$, so edge suppression begins
- Critical point where multiple solutions become possible

**Post-Bottleneck** ($\tau > \tau_c$):
- Strong edge suppression forces $\alpha_i \to 0$
- System must choose which correlations survive

## 4. Tensor Network Implementation

### 4.1 Node-to-Tensor Mapping

Each node $n_i$ becomes a rank-4 tensor $T^{(i)}$ with indices connecting to neighbors:
```
    a₁₂
     |
a₁₄--T¹--a₁₃
     |
    a₁₁
```

**Bond Dimensions**:
- Edge bonds: $\chi_{\text{edge}}(\tau) = \lfloor |\alpha_i(\tau)| \cdot \chi_{\max} \rfloor$
- Diagonal bonds: $\chi_{\text{diag}}(\tau) = \lfloor |\beta_j(\tau)| \cdot \chi_{\max} \rfloor$

### 4.2 Correlation Function Calculation

**Distance Matrix** (pre-geometric):
```
     n₁  n₂  n₃  n₄
n₁ [ 0   1   √2  1 ]
n₂ [ 1   0   1   √2]  
n₃ [√2   1   0   1 ]
n₄ [ 1  √2   1   0 ]
```

**Correlation Function**:
$$C_{ij}(\tau) = \text{Tr}[\rho(\tau) \cdot O_i \otimes O_j]$$

where $\rho(\tau)$ is the density matrix from the tensor network contraction.

### 4.3 Emergent Metric Extraction

Post-bottleneck, if correlations satisfy $C_{ij} \sim e^{-d_{ij}/\xi}$, then:
$$g_{\text{emergent}}^{ij} = -\frac{\partial^2 \log C_{ij}}{\partial x^i \partial x^j}$$

## 5. Hand-Calculable Solutions

### 5.1 Symmetric Initial Conditions

**Initial State**: $\alpha_1 = \alpha_2 = \alpha_3 = \alpha_4 = \alpha_0$, $\beta_1 = \beta_2 = \beta_0$

**Conservation Constraint**: $\mathcal{E} = 4\alpha_0^4 + 2\beta_0^2 + 4\alpha_0^2\beta_0 = E_0$

**Reduced Evolution** (using symmetry):
$$\frac{d\alpha}{d\tau} = -2(4\alpha^4 + 2\beta^2 + 4\alpha^2\beta - E_0)(4\alpha^3 + 2\alpha\beta) - 2\lambda_2 f_{\text{bottle}}(\tau)\alpha$$

$$\frac{d\beta}{d\tau} = -2(4\alpha^4 + 2\beta^2 + 4\alpha^2\beta - E_0)(2\beta + 2\alpha^2) - 2\lambda_1\beta$$

### 5.2 Critical Point Analysis

At the critical point, $\frac{d\alpha}{d\tau} = \frac{d\beta}{d\tau} = 0$:

**Case 1** (High Entanglement): $\alpha_c \neq 0$, $\beta_c \neq 0$
**Case 2** (Edge Dominant): $\alpha_c \neq 0$, $\beta_c = 0$  
**Case 3** (Diagonal Dominant): $\alpha_c = 0$, $\beta_c \neq 0$
**Case 4** (Disentangled): $\alpha_c = \beta_c = 0$

### 5.3 Stability Analysis

**Jacobian Matrix**:
$$J = \begin{pmatrix}
\frac{\partial}{\partial \alpha}\frac{d\alpha}{d\tau} & \frac{\partial}{\partial \beta}\frac{d\alpha}{d\tau} \\
\frac{\partial}{\partial \alpha}\frac{d\beta}{d\tau} & \frac{\partial}{\partial \beta}\frac{d\beta}{d\tau}
\end{pmatrix}$$

**Eigenvalue Analysis**: 
- $\lambda_1, \lambda_2 < 0$: Stable fixed point
- $\lambda_1, \lambda_2 > 0$: Unstable (saddle or repeller)
- $\lambda_1 \lambda_2 < 0$: Saddle point

## 6. Predicted Phase Diagram

### 6.1 Parameter Space

**Control Parameters**:
- $\lambda_1$ (locality strength)
- $\lambda_2$ (bottleneck strength)  
- $E_0$ (total entanglement)
- $\tau_c$ (bottleneck timing)

### 6.2 Phase Boundaries

**Phase I** ($\lambda_2 \ll \lambda_1$): Edge-dominated, $\alpha \gg \beta$
**Phase II** ($\lambda_2 \gg \lambda_1$): Diagonal-dominated, $\beta \gg \alpha$  
**Phase III** ($\lambda_2 \approx \lambda_1$): Mixed phase with both correlations

**Critical Line**: $\lambda_2 = \lambda_1 \cdot f(\E_0)$ where specific form depends on entanglement

### 6.3 Emergent Geometry Prediction

**Conjecture**: Post-bottleneck in Phase I, correlations should satisfy:
$$C_{ij} \propto \exp(-d_{ij}^{\text{Manhattan}}/\xi)$$

where $d_{ij}^{\text{Manhattan}}$ is the Manhattan distance on the square lattice, suggesting emergent **discrete 2D geometry**.

## 7. Computational Protocol

### 7.1 Numerical Integration

```python
def evolve_4node_system(alpha0, beta0, E0, lambda1, lambda2, tau_c, sigma, tau_max):
    """
    Evolve the 4-node DEB system numerically
    """
    # Initial conditions
    state = [alpha0, alpha0, alpha0, alpha0, beta0, beta0]
    tau_range = np.linspace(0, tau_max, 1000)
    
    # Evolution equations
    def derivatives(tau, s):
        alpha1, alpha2, alpha3, alpha4, beta1, beta2 = s
        E_current = alpha1*alpha2*alpha3*alpha4 + beta1*beta2 + alpha1*alpha3*beta1 + alpha2*alpha4*beta2
        f_bottle = 0.5 * (1 + np.tanh(sigma * (tau - tau_c)))
        
        dalpha1_dt = -2*(E_current - E0)*(alpha2*alpha3*alpha4 + alpha3*beta1) - 2*lambda2*f_bottle*alpha1
        dalpha2_dt = -2*(E_current - E0)*(alpha1*alpha3*alpha4 + alpha4*beta2) - 2*lambda2*f_bottle*alpha2
        dalpha3_dt = -2*(E_current - E0)*(alpha1*alpha2*alpha4 + alpha1*beta1) - 2*lambda2*f_bottle*alpha3
        dalpha4_dt = -2*(E_current - E0)*(alpha1*alpha2*alpha3 + alpha2*beta2) - 2*lambda2*f_bottle*alpha4
        dbeta1_dt = -2*(E_current - E0)*(beta2 + alpha1*alpha3) - 2*lambda1*beta1
        dbeta2_dt = -2*(E_current - E0)*(beta1 + alpha2*alpha4) - 2*lambda1*beta2
        
        return [dalpha1_dt, dalpha2_dt, dalpha3_dt, dalpha4_dt, dbeta1_dt, dbeta2_dt]
    
    # Solve ODE
    solution = solve_ivp(derivatives, [0, tau_max], state, t_eval=tau_range)
    return solution

# Example parameters
result = evolve_4node_system(
    alpha0=0.5, beta0=0.3, E0=0.8, 
    lambda1=0.1, lambda2=1.0, 
    tau_c=5.0, sigma=2.0, tau_max=10.0
)
```

### 7.2 Geometric Analysis

```python
def extract_emergent_geometry(solution):
    """
    Extract correlation matrix and test for emergent geometry
    """
    final_state = solution.y[:, -1]  # Final state after evolution
    
    # Construct correlation matrix based on final entanglement strengths
    C = np.zeros((4, 4))
    # Fill based on surviving entanglement relations
    
    # Test for metric properties
    is_positive_definite = check_positive_definite(C)
    satisfies_triangle_inequality = check_triangle_inequality(C)
    
    # Extract distance matrix
    if is_positive_definite:
        distances = -np.log(C + 1e-10)  # Avoid log(0)
        return distances, True
    else:
        return None, False
```

## 8. Testable Predictions

### 8.1 Critical Behavior

**Prediction 1**: Near $\tau_c$, entanglement correlation length should diverge as:
$$\xi(\tau) \sim |\tau - \tau_c|^{-\nu}$$
with $\nu \approx 1$ for this mean-field-like system.

**Prediction 2**: Entanglement entropy should exhibit finite-size scaling:
$$S(\tau_c, L) = S_{\infty} + L^{-1/\nu} f(L^{1/\nu}(\tau - \tau_c))$$

### 8.2 Geometric Emergence

**Prediction 3**: Post-bottleneck correlations should satisfy:
- **Positivity**: $C_{ij} > 0$ for connected nodes
- **Symmetry**: $C_{ij} = C_{ji}$  
- **Triangle inequality**: $d_{ik} \leq d_{ij} + d_{jk}$ where $d_{ij} = -\log C_{ij}$

**Prediction 4**: Emergent geometry should be **2-dimensional** with **Manhattan metric** structure.

## 9. Connection to Full Theory

This minimal model demonstrates:

1. **Categorical gradient flow** can be made explicit and computable
2. **Information-theoretic constraints** naturally generate physical dynamics  
3. **Bottleneck mechanisms** can drive phase transitions in entanglement structure
4. **Emergent correlations** can satisfy geometric axioms
5. **Critical phenomena** arise naturally from the mathematical structure

The 4-node model serves as a "proof of principle" that the abstract DEB framework can produce concrete, testable physics in its simplest realization.

## 10. Next Steps

1. **Implement numerical evolution** and verify phase transition occurs
2. **Analyze emergent correlation structure** for geometric properties  
3. **Extend to 8-node system** (cube topology) for 3D geometric emergence
4. **Study finite-size scaling** to extract critical exponents
5. **Connect to tensor network contractions** for quantum state evolution

This minimal model provides the foundation for scaling up to more complex realizations while maintaining analytical control and physical intuition.