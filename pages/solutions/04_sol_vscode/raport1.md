# Rzut ukośny — od trajektorii parabolicznej do oporu powietrza

*Raport obliczeniowy i przykład wykorzystania Markdown w dokumentacji naukowej.*

**Temat:** Dwuwymiarowy ruch masy w polu grawitacyjnym z uwzględnieniem oporu ośrodka.  
**Metoda:** Rozwiązania analityczne, całkowanie numeryczne w Pythonie i interpretacja wykresów.  
**Charakter danych:** Przykład modelowy; wszystkie wykresy przedstawiają obliczenia dla indywidualnych parametrów początkowych.

Galileusz jako pierwszy wykazał, że w warunkach idealnych:
> Ruch rzutu ukośnego składa się z dwóch niezależnych ruchów: jednostajnego w poziomie oraz jednostajnie zmiennego w pionie.

W rzeczywistych warunkach atmosferycznych siła oporu aerodynamicznego drastycznie zmienia postać tego ruchu. Połączenie siły grawitacji i oporu lepkiego prowadzi do układu równań różniczkowych, którego rozwiązanie pozwala wyznaczyć rzeczywisty zasięg, czas lotu oraz optymalny kąt strzału. W tym raporcie analizujemy przypadek dla zadanych parametrów początkowych: prędkości $v_0 = 37 \, \mathrm{m/s}$ oraz kąta $\alpha = 3^\circ$.

## Spis treści

1. [Cel i model fizyczny](#1-cel-i-model-fizyczny)
2. [Model idealny (bez oporu powietrza)](#2-model-idealny-bez-oporu-powietrza)
3. [Model z oporem powietrza](#3-model-z-oporem-powietrza)
4. [Analiza numeryczna i porównanie trajektorii](#4-analiza-numeryczna-i-porównanie-trajektorii)
5. [Zależność zasięgu od kąta wyrzutu](#5-zależność-zasięgu-od-kąta-wyrzutu)
6. [Kod źródłowy symulacji](#6-kod-źródłowy-symulacji)
7. [Wnioski](#7-wnioski)

---

## 1. Cel i model fizyczny

Głównym celem raportu jest zbadanie wpływu oporu powietrza na ruch ciała rzuconego ukośnie, wyprowadzenie równań kinematycznych oraz wyznaczenie różnic w kluczowych parametrach lotu (zasięg, wysokość maksymalna, czas lotu).

### 1.1. Założenia projektowe
- Ruch odbywa się w jednorodnym polu grawitacyjnym ziemi, gdzie $g = 9.81 \, \mathrm{m/s^2}$.
- Masa ciała wynosi $m = 0.15 \, \mathrm{kg}$ (odpowiednik piłki baseballowej).
- Siła oporu powietrza jest proporcjonalna do prędkości (opór Stokesa): $F_{\text{op}} = -b \cdot v$, gdzie współczynnik oporu wynosi $b = 0.02 \, \mathrm{N \cdot s / m}$.
- **Parametry początkowe (zgodnie z wytycznymi):**
  - Prędkość początkowa: $v_0 = 37 \, \mathrm{m/s}$
  - Kąt początkowy: $\alpha = 3^\circ$ (zamieniony na radiany: $\alpha = 3 \cdot \pi / 180 \approx 0.05236 \, \mathrm{rad}$)

---

## 2. Model idealny (bez oporu powietrza)

W modelu bez oporu powietrza ($b = 0$) na ciało działa wyłącznie siła ciężkości $F_g = mg$ skierowana w dół.

### 2.1. Równania ruchu
Drugie prawo Newtona dla składowych osi układu współrzędnych przyjmuje postać:

$$
m \frac{d^2x}{dt^2} = 0, \quad m \frac{d^2y}{dt^2} = -mg
$$

Po skróceniu masy i jednokrotnym zcałkowaniu z warunkami początkowymi $v_{x0} = v_0 \cos\alpha$ oraz $v_{y0} = v_0 \sin\alpha$ otrzymujemy składowe prędkości:

$$
v_x(t) = v_0 \cos\alpha, \quad v_y(t) = v_0 \sin\alpha - gt
$$

Ponowne całkowanie daje równania położenia w funkcji czasu:

$$
x(t) = v_0 t \cos\alpha, \quad y(t) = v_0 t \sin\alpha - \frac{1}{2}gt^2
$$

### 2.2. Wyznaczenie trajektorii i parametrów lotu
Eliminując czas $t = \frac{x}{v_0 \cos\alpha}$, uzyskujemy klasyczne równanie paraboli rzutu:

$$
y(x) = x \tan\alpha - \frac{g}{2 v_0^2 \cos^2\alpha} x^2
$$

Analityczny czas lotu $t_{\text{lot}}$ (dla $y = 0$) oraz maksymalny zasięg $Z$ wynoszą:

$$
t_{\text{lot}} = \frac{2 v_0 \sin\alpha}{g}, \quad Z = \frac{v_0^2 \sin(2\alpha)}{g}
$$

Dla zadanych parametrów ($v_0 = 37$, $\alpha = 3^\circ$):
- $t_{\text{lot}} \approx 0.3957 \, \mathrm{s}$
- $Z \approx 14.60 \, \mathrm{m}$

---

## 3. Model z oporem powietrza

Gdy uwzględniamy opór powietrza, siła wypadkowa wynosi $F = F_g + F_{\text{op}}$. Układ równań różniczkowych przyjmuje postać:

$$
m \ddot{x} = -b \dot{x}, \quad m \ddot{y} = -mg - b \dot{y
$$

Wprowadzając stałą relaksacji $\gamma = \frac{b}{m}$, równania przyjmują formę:

$$
\ddot{x} + \gamma \dot{x} = 0, \quad \ddot{y} + \gamma \dot{y} = -g
$$

### 3.1. Rozwiązanie analityczne
Rozwiązując te równania metodą rozdzielania zmiennych z uwzględnieniem warunków początkowych, otrzymujemy dokładne wzory na położenie:

$$
x(t) = \frac{v_0 \cos\alpha}{\gamma} \left( 1 - e^{-\gamma t} \right)
$$

$$
y(t) = \frac{1}{\gamma} \left( v_0 \sin\alpha + \frac{g}{\gamma} \right) \left( 1 - e^{-\gamma t} \right) - \frac{g}{\gamma} t
$$

Z powodu obecności wyrazu liniowego i eksponencjalnego w równaniu osi $y$, zasięg i czas lotu z oporem powietrza nie mogą być wyznaczone jawnie metodami algebraicznymi — wymagają użycia metod numerycznych.

---

## 4. Analiza numeryczna i porównanie trajektorii

Dla zadanych parametrów wygenerowano trajektorie lotu. Z powodu bardzo małego kąta początkowego ($\alpha = 3^\circ$), tor lotu jest płaski, a różnice spowodowane oporem aerodynamicznym uwidaczniają się głównie pod koniec fazy opadania.

![Porównanie trajektorii rzutu ukośnego](files/rzut/trajektoria.png)

*Rysunek 1. Porównanie toru lotu bez oporu (parabola) oraz z uwzględnieniem oporu powietrza (krzywa balistyczna).*

![Przebiegi prędkości w czasie](files/rzut/predkosc.png)

*Rysunek 2. Składowe prędkości $v_x$ i $v_y$ w funkcji czasu dla obu modeli.*

---

## 5. Zależność zasięgu od kąta wyrzutu

W modelu idealnym maksymalny zasięg osiągany jest dla kąta $\alpha = 45^\circ$. Wprowadzenie oporu powietrza sprawia, że optymalny kąt wyrzutu ulega zmniejszeniu, ponieważ pocisk spędzający więcej czasu w powietrzu traci zbyt dużo energii kinetycznej.

![Zasięg w funkcji kąta](files/rzut/katy.png)

*Rysunek 3. Wpływ kąta początkowego na końcowy zasięg rzutu dla ustalonej prędkości początkowej $v_0 = 37 \, \mathrm{m/s}$.*

---

## 6. Kod źródłowy symulacji

Poniższy kod napisany w języku Python (wykorzystujący biblioteki `numpy` i `matplotlib`) służy do pełnego odtworzenia powyższych wykresów. Pliki automatycznie zapisują się w dedykowanym folderze zasobów rozwiązania.

```python
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Konfiguracja ścieżek zapisu
OUT = Path("files/rzut")
OUT.mkdir(parents=True, exist_ok=True)

# Parametry wejściowe zgodne z indeksem
v0 = 37.0      # Prędkość początkowa (m/s)
alpha_deg = 3.0 # Kąt początkowy (stopnie)
alpha = np.radians(alpha_deg)
g = 9.81       # Przyspieszenie ziemskie (m/s^2)
m = 0.15       # Masa (kg)
b = 0.02       # Współczynnik oporu (N*s/m)
gamma = b / m  # Stała relaksacji

# 1. Obliczenie trajektorii
t_max_ideal = (2 * v0 * np.sin(alpha)) / g
t_eval = np.linspace(0, t_max_ideal * 1.1, 1000)

# Model idealny
x_id = v0 * t_eval * np.cos(alpha)
y_id = v0 * t_eval * np.sin(alpha) - 0.5 * g * t_eval**2
vx_id = np.ones_like(t_eval) * v0 * np.cos(alpha)
vy_id = v0 * np.sin(alpha) - g * t_eval

# Model z oporem
x_op = (v0 * np.cos(alpha) / gamma) * (1 - np.exp(-gamma * t_eval))
y_op = (1 / gamma) * (v0 * np.sin(alpha) + g / gamma) * (1 - np.exp(-gamma * t_eval)) - (g / gamma) * t_eval
vx_op = v0 * np.cos(alpha) * np.exp(-gamma * t_eval)
vy_op = (v0 * np.sin(alpha) + g / gamma) * np.exp(-gamma * t_eval) - g / gamma

# Obcinanie do momentu uderzenia w ziemię (y >= 0)
idx_id = np.where(y_id >= 0)[0]
idx_op = np.where(y_op >= 0)[0]

# Wykres 1: Trajektoria
fig1, ax1 = plt.subplots(figsize=(10, 4), layout="constrained")
ax1.plot(x_id[idx_id], y_id[idx_id], label="Bez oporu (idealny)", color="#2463A6", lw=2)
ax1.plot(x_op[idx_op], y_op[idx_op], label="Z oporem lepkym", color="#D47722", lw=2)
ax1.set_xlabel("Dystans x [m]")
ax1.set_ylabel("Wysokość y [m]")
ax1.set_title("Trajektoria rzutu ukośnego (v0 = 37 m/s, α = 3°)", loc="left", weight="bold")
ax1.grid(True, alpha=0.2)
ax1.legend()
fig1.savefig(OUT / "trajektoria.png", dpi=180)
plt.close(fig1)

# Wykres 2: Prędkości
fig2, ax2 = plt.subplots(figsize=(10, 4), layout="constrained")
ax2.plot(t_eval[idx_id], vx_id[idx_id], label="vx (bez oporu)", color="#2463A6", ls="--")
ax2.plot(t_eval[idx_op], vx_op[idx_op], label="vx (z oporem)", color="#2463A6")
ax2.plot(t_eval[idx_id], vy_id[idx_id], label="vy (bez oporu)", color="#D47722", ls="--")
ax2.plot(t_eval[idx_op], vy_op[idx_op], label="vy (z oporem)", color="#D47722")
ax2.set_xlabel("Czas t [s]")
ax2.set_ylabel("Prędkość [m/s]")
ax2.set_title("Składowe prędkości w funkcji czasu", loc="left", weight="bold")
ax2.grid(True, alpha=0.2)
ax2.legend()
fig2.savefig(OUT / "predkosc.png", dpi=180)
plt.close(fig2)

# Wykres 3: Zasięg od kąta
katy = np.linspace(0, 90, 500)
zasieg_id = (v0**2 * np.sin(2 * np.radians(katy))) / g
zasieg_op = []

for k_deg in katy:
    k_rad = np.radians(k_deg)
    t_przestrzen = np.linspace(0, 10, 2000)
    y_test = (1 / gamma) * (v0 * np.sin(k_rad) + g / gamma) * (1 - np.exp(-gamma * t_przestrzen)) - (g / gamma) * t_przestrzen
    idx_ziemia = np.where(y_test < 0)[0]
    if len(idx_ziemia) > 0:
        t_hit = t_przestrzen[idx_ziemia[0]]
        x_hit = (v0 * np.cos(k_rad) / gamma) * (1 - \
np.exp(-gamma * t_hit))
        zasieg_op.append(x_hit)
    else:
        zasieg_op.append(0)

fig3, ax3 = plt.subplots(figsize=(10, 4), layout="constrained")
ax3.plot(katy, zasieg_id, color="#2463A6", label="Bez oporu")
ax3.plot(katy, zasieg_op, color="#D47722", label="Z oporem")
ax3.set_xlabel("Kąt początkowy α [°]")
ax3.set_ylabel("Zasięg maksymalny [m]")
ax3.set_title("Zasięg rzutu w funkcji kąta początkowego", loc="left", weight="bold")
ax3.grid(True, alpha=0.2)
ax3.legend()
fig3.savefig(OUT / "katy.png", dpi=180)
plt.close(fig3)
print("Wykresy zostały pomyślnie wygenerowane.")
```

---

## 7. Wnioski

1. Dla bardzo małego kąta początkowego ($\alpha = 3^\circ$), ruch w pionie trwa bardzo krótko (poniżej 0.4 sekundy). W tym reżimie siła oporu powietrza ma mniejszy czas na drastyczne skrócenie trajektorii w porównaniu do wysokich rzutów balistycznych.
2. Mimo to, obecność oporu powietrza zauważalnie zmniejsza końcowy zasięg rzutu o stałą wartość wynikającą z wykładniczego tłumienia prędkości poziomej $v_x$.

