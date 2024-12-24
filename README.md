# PyPolynomial
PyPolynomial is a project that implements three ideas from algebra:
* Rings
* Fields
* Polynomials

To use PyPolynomial, you must include the file or the code in your project directory. As of right now, this project is not part of the python package index, and is mostly meant as a fun showcase of some algebra.
PyPolynomial has no dependencies, but is compatible with objects from other libraries if you define the ```Ring``` member functions properly.
## Rings
Rings are collection of the form $(R, +, \bullet)$, where:
* $R$ is a set,
* and $+ : R^2 \rightarrow R$ and $\bullet : R^2 \rightarrow R$ are functions such that the [ring axioms](https://en.wikipedia.org/wiki/Ring_(mathematics)) are satisfied.

In PyPolynomial, ```Ring``` is a class that requires the following arguments:
* ```add```: a function that takes as arguments two elements $a,b \in R$ and returns $a+b$.
* ```sub```: a function that takes as arguments two elements $a,b \in R$ and returns $a-b$. This is necessary for calculating additive inverses, since not every ring is endowed with a multiplicative identity.
* ```mult```: a  function that takes as arguments two elements $a,b \in R$ and returns $a \bullet b$.
* ```contains```: a function that takes as an argument one object $a$ and returns True if $a \in R$ and False otherwise. This function is used to define the set $R$.
* ```zero```: an object corresponding to the zero element, $0_R \in R$.

The following arguments are optional but highly encouraged:
* ```real_subset```: a boolean, True if $R$ is a subset of $\mathbb{R}$, and False otherwise. Default value: True
* ```name```: a string representing the name of the ring (e.g. $\mathbb{Q, C, R}$). Default value: ""
* ```to_str```: a function that takes as an argument an element $a \in R$ and returns the string representation of that element. If you want elements of $R$ to be displayed differently than the str() method, use this argument. Default value: None

Take for example our definition of the ring of integers, $\mathbb{Z}$
```python 
def add(a,b):
    return a+b
def sub(a,b):
    return a-b
def mult(a,b):
    return a*b
def inverse(a):
    return 1/a
def contains(a):
    if type(a) == type(1):
        return True
    return False
Z = Ring(add, sub, mult, contains, zero = 0, real_subset = True, name = "Z")
```
This framework gives you the flexibility to create many different kinds of rings by simply defining their structure. The benefit is that any ring you define is automatically compatible with the ```Polynomial``` class, assuming its member functions satisfy the ring axioms.

PyPolynomial comes with the premade rings including $\mathbb{Z, Q}$ and $\mathbb{C}$, where $\mathbb{C}$ is the field of Gaussian Rationals. $\mathbb{R}$ is currently not implemented since I did not code support for dealing with infinite-precision real numbers in this first version.

## Fields
Fields are collections $(F, +, \bullet)$, where
* $F$ is a set, and
* $+$ and $\bullet$ are the same as in the definition of Rings, but satisfying the [field axioms](https://en.wikipedia.org/wiki/Field_(mathematics)) in addition to the ring axioms.

 In PyPolynomial, ```Field``` is a subclass of ```Ring```. In addition to the arguments required to construct a ring, fields require the additional arguments:
 * ```identity```: an object representing the identity element, $1_F \in F$.
 * ```inverse```: a function that takes as an argument an element $a \in F$ and returns its multiplicative inverse $a^{-1} \in F$

## Polynomials
Given a ring $R$, we say $f(x)$ is a polynomial over that ring if $f(x) = a_0 + a_1 x + a_2 x^2 + ... + a_n x^n$, where $a_i \in R$ for $i \in \{0,1 \dots n\}$, and $x$ is an element of an extension ring of $R$ such that $\forall b \in R, bx = xb$.

The set of all polynomials, equipped with polynomial addition and multiplication, $R[x]$, is a ring. 

In PyPolynomial, ```Polynomial``` is a class that requires two arguments:
* ```coeffs```: a dictionary where the keys are the powers and the values are the coefficients. the coefficients must all be elements of the same ring.
* ```R```: a Ring object. This ring contains all of the coefficients of the polynomial, and is responsible for defining basic operations on the polynomial.

Consider, for example, the following polynomial over the integers (which are defined as part of PyPolynomial):
```python
coeffs = {0:1,
          2:3,
          5:-1}
f = Polynomial(coeffs, Z)
f
```
f is now the polynomial with $1$ as its constant coefficient, $3$ as the coefficient of $x^2$, and $-1$ as the coefficient of $x^5$, as indicated by the output of the previous code block:
```plaintext
Polynomial(1 + 3x^2 - x^5, R = Z)
```
PyPolynomial automatically converts a polynomial to its induced function, enabling "calling" a polynomial as you would a function:
```python
print("f evaluated at 1 is:", f(1))
print("f evaluated at 0 is:", f(0))
```
```plaintext
f evaluated at 1 is: 3
f evaluated at 0 is: 1
```
### Operations on Polynomials
Any binary operations on polynomials require that they both have coefficients in the same field. This means that they must both use the same ring as their "R" argument in their constructors. Even if operations between two polynomials are well-defined in one of their rings (say adding a polynomial in $\mathbb{Z}[x]$ to one in $\mathbb{Q}[x]$), PyPolynomial will treat this as undefined behavior and raise an exception.

Basic arithmetic between any polynomials is fully supported:
``` python
f = Polynomial({0:1, 2:1}, R = Z)
g = Polynomial({1:2, 2:2}, R = Z)
print("(f+g)(x) =", f+g)
print("(fg)(x) =", f*g)
```
```plaintext
(f+g)(x) = 1 + 2x + 3x^2
(fg)(x) = 2x + 2x^2 + 2x^3 + 2x^4
```
For polynomials defined over fields, polynomial division is also well-defined (with a remainder if the divisor is not a factor of the dividend):
```python
u = Polynomial({0:0.5, 1:1, 3:4, 5:-2}, R = Q)
v = Polynomial({1:2, 2:2}, R = Q)
q, r = u/v
print("u(x) =", u)
print("v(x) =", v)
print("quotient of u(x)/v(x):", q)
print("remainder of u(x)/v(x):", r)
```
```plaintext
u(x) = 0.5 + x + 4x^3 - 2x^5
v(x) = 2x + 2x^2
quotient of u(x)/v(x): -1.0 + x + x^2 - x^3
remainder of u(x)/v(x): 0.5 + 3.0x
```
Where division is defined, we can also take the greatest common divisor of two polynomials, denoted $\gcd(f(x), g(x))$. PyPolynomial adopts the convention that $\gcd(f(x), g(x))$ is the monic polynomial of highest degree that divides both $f(x)$ and $g(x)$.
```python
print(gcd(u,v))
```
```plaintext
1.0
```
## Extension Fields
PyPolynomial was designed to deal with relatively abstract polynomials. Given a field $F$ and an irreducible polynomial $p(x)$, we can construct the quotient ring $F[x]/p(x)$ using the PyPolynomial function ```poly_quotient_ring```.
```python
p = Polynomial({0:1, 2:1}, R = Q)
QMod_p = poly_quotient_ring(Q)
print(QMod_p.name)
```
```plaintext
'Q/(1 + x^2)'
```
This represents the field $\mathbb{Q}$ algebraically extended by $i$, the root of $1+x^2$ (since $-i$ is in this extension, we only consider the first root).
We can define polynomials in this new field. The coefficients are any of the elements of $\mathbb{Q}/(1+x^2)$, which are exactly the equivalence classes of all the polynomials in $\mathbb{Q}[x]$ with degree strictly less than $1+x^2$. Here is an example:
```python
f_coeffs = {
            1 : Polynomial({0:5}, R = p.R),
            2 : Polynomial({0:1, 1:1.5}, R = p.R),
            5 : Polynomial({1:0.25}, R = p.R)
            }
f = Polynomial(f_coeffs, R = QMod_p)
print("f(x) =", f)
```
```plaintext
f(x) = [5]x + [1 + 1.5x]x^2 + [0.25x]x^5
```
Similarly to the modular arithmetic in the integers, if we initialize a polynomial in a polynomial quotient ring using coefficients with degree >= $p(x)$, we simply divide them by $p(x)$ and use their remainder, which is in the same equivalence class. This convention holds for all operations as well:
```python
g_coeffs = {
            1 : Polynomial({0:1, 3:2}, R = p.R),
            2 : Polynomial({0:4, 1:1, 2:3, 3:1}, R = p.R),
            }
g = Polynomial(g_coeffs, R = QMod_p)
# coefficient of 'x' before modding out p(x):
print("first term pre-modding:", g_coeffs[1])
# coefficient of 'x' before modding out p(x):
print("second term pre-modding:", g_coeffs[2])
# coefficients of g(x) after converting the polynomials into their equivalence classes:
print("polynomial post-modding:", g)
```
```plaintext
first term pre-modding: 1 + 2x^3
second term pre-modding: 4 + x + 3x^2 + x^3
polynomial post-modding: [1 - 2.0x]x + [1.0]x^2
```
For any polynomial $f(x) \in F[x]$, if we consider the equivalence class of $f(x)$, $[f(x)]$, then it has an inverse in the field $F[x]/p(x)$. Since PyPoly considers any polynomial over $F[x]$ to be an an element of $F[x]/p(x)$ (after taking its remainder when divided by $p(x)$ ), we can take its inverse:
```python
a = Polynomial({0:1, 1:1}, R = p.R)
a_inv = QMod_p.inv(a)
print("a(x) =", a)
print("a_inv(x) =", a_inv)
print("a(x) * a_inv(x) =", QMod_p.mult(a,a_inv))
```
```plaintext
a(x) = 1 + x
a_inv(x) = 0.5 - 0.5x
a(x) * a_inv(x) = 1.0
```
### Final Reminders
The PyPolynomial module adds an implementation of polynomials that is simple, independent of other libraries, and capable of great versatility should you choose to define your own rings or make use of the extension fields supported by PyPolynomial.
