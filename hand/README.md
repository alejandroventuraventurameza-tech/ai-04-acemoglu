# Handwritten derivations

Phone photos of the steps I checked by hand. Crooked and with crossings-out is the
standard: the point is that the step went through my head, not through the machine.

| File | What it shows |
|---|---|
| _(pending)_ `hand/obs1-crowding-out.jpg` | |
| _(pending)_ `hand/lemma2-maintenance.jpg` | |

## Plan — what to write out (intermediate rigor)

**Page 1: Observation 1 and partial crowding-out (§3.4).** This is the result the assignment
prioritises.
1. From $G(\tau)=2\Phi(\sqrt\tau)-1$, derive $g(\tau)=\phi(\sqrt\tau)/\sqrt\tau$ with the chain rule.
2. Derive $g'(\tau)=-g(\tau)\,\frac{1+\tau}{2\tau}$ with the product rule. *This is the step that
   looks too easy: the entire "AI substitutes for effort" sign rests on it.*
3. Compute $U_{eX}$ and $U_{e\tau_A}$ from $U_e=\Delta_X G(X)\lambda_I g(Y)-e^{1/\varepsilon}$.
4. Use the implicit function theorem to get $\partial e/\partial\tau_A$, then show
   $dY/d\tau_A = a/(a+b)\in(0,1)$. Holding $X$ fixed, AI crowds out learning, but less than
   one-for-one.

**Page 2: why the threshold is $\varepsilon=4$ (Lemma 2).** This is the bridge between the static
FOC and the precision recursion.
1. Show $F(X)>X \iff e > e_m(X)=\dfrac{\Sigma^2X^2}{\lambda_G I(1-\Sigma^2X)}$ (pure algebra).
2. Near $0$: $G(X)\approx\sqrt{2X/\pi}$, so the FOC gives $e\approx\kappa X^{\varepsilon/2}$.
3. Compare the exponents $\varepsilon/2$ and $2$.
4. Note that $F'(0)=1$ when $\varepsilon>2$: linearisation cannot decide stability.

Cross-checks: `sim/verify_static.py` (SymPy) and `lean/` (Lean 4, targets T2–T5).
