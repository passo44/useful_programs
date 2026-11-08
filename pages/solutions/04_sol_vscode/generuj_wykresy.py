from pathlib import Path
from html import escape
import numpy as np
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
OUT = HERE / "files" / "rzut"
OUT.mkdir(parents=True, exist_ok=True)

# Parametry modelu: kula o masie jak w szkicu zadania i liniowy opor lepkosci.
v0 = 34.0
alpha_deg = 3.0
alpha = np.deg2rad(alpha_deg)
g = 9.81
m = 0.15
b = 0.02
gamma = b / m

BLUE, ORANGE, GREEN, PURPLE, INK = (
    "#2463A6", "#D47722", "#168578", "#8455A4", "#233044"
)
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelcolor": INK,
    "text.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.2,
    "lines.linewidth": 2.2,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "svg.fonttype": "none",
})


def pozycja_opor(t, kat):
    """Analityczne x(t), y(t) dla oporu F_d = -b*v."""
    vx0 = v0 * np.cos(kat)
    vy0 = v0 * np.sin(kat)
    x = vx0 * (-np.expm1(-gamma * t)) / gamma
    y = (vy0 + g / gamma) * (-np.expm1(-gamma * t)) / gamma - g * t / gamma
    return x, y


def czas_lotu_opor(kat):
    """Pierwszy dodatni pierwiastek y(t)=0, wyznaczony bisekcja."""
    if np.isclose(kat, 0.0):
        return 0.0
    low = 0.0
    high = max(1.0, 2.0 * v0 * np.sin(kat) / g + 0.1)
    while pozycja_opor(high, kat)[1] > 0:
        high *= 2.0
    for _ in range(80):
        mid = (low + high) / 2.0
        if pozycja_opor(mid, kat)[1] > 0:
            low = mid
        else:
            high = mid
    return (low + high) / 2.0


def bez_oporu(t, kat):
    vx0 = v0 * np.cos(kat)
    vy0 = v0 * np.sin(kat)
    x = vx0 * t
    y = vy0 * t - 0.5 * g * t**2
    vx = np.full_like(t, vx0)
    vy = vy0 - g * t
    return x, y, vx, vy


def z_oporem(t, kat):
    vx0 = v0 * np.cos(kat)
    vy0 = v0 * np.sin(kat)
    exp_term = np.exp(-gamma * t)
    x, y = pozycja_opor(t, kat)
    vx = vx0 * exp_term
    vy = (vy0 + g / gamma) * exp_term - g / gamma
    return x, y, vx, vy


def zapisz(fig, nazwa):
    fig.savefig(OUT / nazwa, dpi=180)
    plt.close(fig)


def zapisz_svg(nazwa, tytul, xlabel, ylabel, serie):
    width, height = 720, 390
    left, right, top, bottom = 76, 22, 58, 58
    plot_width, plot_height = width - left - right, height - top - bottom
    xs = np.concatenate([np.asarray(s[0]) for s in serie])
    ys = np.concatenate([np.asarray(s[1]) for s in serie])
    x_min, x_max = float(xs.min()), float(xs.max())
    y_min, y_max = min(0.0, float(ys.min())), max(0.0, float(ys.max()))
    if x_min == x_max:
        x_max = x_min + 1.0
    if y_min == y_max:
        y_max = y_min + 1.0
    y_pad = 0.06 * (y_max - y_min)
    y_min, y_max = y_min - y_pad, y_max + y_pad
    px = lambda value: left + (float(value) - x_min) / (x_max - x_min) * plot_width
    py = lambda value: top + (y_max - float(value)) / (y_max - y_min) * plot_height
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<g font-family="DejaVu Sans, sans-serif" fill="#233044">',
        f'<text x="{left}" y="27" font-size="16" font-weight="bold">{escape(tytul)}</text>',
    ]
    for index in range(5):
        x_value = x_min + (x_max - x_min) * index / 4
        y_value = y_min + (y_max - y_min) * index / 4
        x_pos, y_pos = px(x_value), py(y_value)
        parts.append(f'<path d="M {x_pos:.1f} {top} V {height-bottom} M {left} {y_pos:.1f} H {width-right}" stroke="#d7dee5" stroke-width="1"/>')
        parts.append(f'<text x="{x_pos:.1f}" y="{height-bottom+18}" text-anchor="middle" font-size="10">{x_value:.3g}</text>')
        parts.append(f'<text x="{left-9}" y="{y_pos+3:.1f}" text-anchor="end" font-size="10">{y_value:.3g}</text>')
    parts.append(f'<path d="M {left} {top} V {height-bottom} H {width-right}" fill="none" stroke="#233044" stroke-width="1.2"/>')
    for values_x, values_y, label, color in serie:
        step = max(1, len(values_x) // 35)
        points = list(zip(np.asarray(values_x)[::step], np.asarray(values_y)[::step]))
        if points[-1] != (values_x[-1], values_y[-1]):
            points.append((values_x[-1], values_y[-1]))
        point_text = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in points)
        parts.append(f'<polyline points="{point_text}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
    for index, (_, _, label, color) in enumerate(serie):
        legend_y = top + 15 + index * 17
        parts.append(f'<path d="M {width-170} {legend_y} h 18" stroke="{color}" stroke-width="2.5"/>')
        parts.append(f'<text x="{width-146}" y="{legend_y+4}" font-size="10">{escape(label)}</text>')
    parts.extend([
        f'<text x="{left+plot_width/2}" y="{height-9}" text-anchor="middle" font-size="12">{escape(xlabel)}</text>',
        f'<text x="18" y="{top+plot_height/2}" text-anchor="middle" font-size="12" transform="rotate(-90 18 {top+plot_height/2})">{escape(ylabel)}</text>',
        '</g></svg>',
    ])
    (OUT / nazwa).write_text("\n".join(parts), encoding="utf-8")


# Czasy zderzenia i wielkosci charakterystyczne dla zadanego kata.
t_hit_ideal = 2.0 * v0 * np.sin(alpha) / g
t_hit_drag = czas_lotu_opor(alpha)
zasięg_ideal = v0**2 * np.sin(2.0 * alpha) / g
x_hit_drag = pozycja_opor(t_hit_drag, alpha)[0]
t_apex_ideal = v0 * np.sin(alpha) / g
t_apex_drag = np.log1p(gamma * v0 * np.sin(alpha) / g) / gamma
h_apex_drag = pozycja_opor(t_apex_drag, alpha)[1]

# Siatki koncza sie dokladnie w chwili ladowania, bez obcinania wykresow.
t_ideal = np.linspace(0.0, t_hit_ideal, 140)
t_drag = np.linspace(0.0, t_hit_drag, 140)
x_i, y_i, vx_i, vy_i = bez_oporu(t_ideal, alpha)
x_d, y_d, vx_d, vy_d = z_oporem(t_drag, alpha)

# 1. Trajektorie w przestrzeni.
fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
ax.plot(x_i, y_i, color=BLUE, label="Bez oporu")
ax.plot(x_d, y_d, color=ORANGE, label="Opór liniowy")
ax.scatter([0, zasięg_ideal, x_hit_drag], [0, 0, 0],
           color=[INK, BLUE, ORANGE], s=28, zorder=3)
ax.set(xlabel="Położenie poziome x [m]", ylabel="Wysokość y [m]")
ax.set_title("Trajektoria dla v₀ = 34 m/s i α = 3°", loc="left")
ax.legend()
zapisz(fig, "trajektoria.png")
zapisz_svg("trajektoria.svg", "Trajektoria rzutu ukośnego", "Położenie x [m]", "Wysokość y [m]", [
    (x_i, y_i, "Bez oporu", BLUE), (x_d, y_d, "Opór liniowy", ORANGE)
])

# 2. Wspolrzedne w czasie.
fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
ax.plot(t_ideal, x_i, color=BLUE, label="Bez oporu")
ax.plot(t_drag, x_d, color=ORANGE, label="Opór liniowy")
ax.set(xlabel="Czas t [s]", ylabel="Położenie x [m]")
ax.set_title("Ruch poziomy", loc="left")
ax.legend()
zapisz(fig, "x_czas.png")
zapisz_svg("x_czas.svg", "Ruch poziomy", "Czas t [s]", "Położenie x [m]", [
    (t_ideal, x_i, "Bez oporu", BLUE), (t_drag, x_d, "Opór liniowy", ORANGE)
])

fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
ax.plot(t_ideal, y_i, color=BLUE, label="Bez oporu")
ax.plot(t_drag, y_d, color=ORANGE, label="Opór liniowy")
ax.axhline(0, color=INK, lw=0.8)
ax.set(xlabel="Czas t [s]", ylabel="Wysokość y [m]")
ax.set_title("Ruch pionowy", loc="left")
ax.legend()
zapisz(fig, "y_czas.png")
zapisz_svg("y_czas.svg", "Ruch pionowy", "Czas t [s]", "Wysokość y [m]", [
    (t_ideal, y_i, "Bez oporu", BLUE), (t_drag, y_d, "Opór liniowy", ORANGE)
])

# 3. Skladowe predkosci.
fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True, layout="constrained")
axes[0].plot(t_ideal, vx_i, color=BLUE, label="Bez oporu")
axes[0].plot(t_drag, vx_d, color=ORANGE, label="Opór liniowy")
axes[0].set_ylabel("Prędkość vₓ [m/s]")
axes[0].set_title("Składowa pozioma", loc="left")
axes[0].legend(ncol=2)
axes[1].plot(t_ideal, vy_i, color=BLUE, label="Bez oporu")
axes[1].plot(t_drag, vy_d, color=ORANGE, label="Opór liniowy")
axes[1].axhline(0, color=INK, lw=0.8)
axes[1].set(xlabel="Czas t [s]", ylabel="Prędkość vᵧ [m/s]")
axes[1].set_title("Składowa pionowa", loc="left")
fig.suptitle("Składowe prędkości", fontweight="bold")
zapisz(fig, "predkosci.png")

# 4. Wartosc predkosci i przyspieszenia.
speed_i = np.hypot(vx_i, vy_i)
speed_d = np.hypot(vx_d, vy_d)
accel_d = np.hypot(-gamma * vx_d, -g - gamma * vy_d)
fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True, layout="constrained")
axes[0].plot(t_ideal, speed_i, color=BLUE, label="Bez oporu")
axes[0].plot(t_drag, speed_d, color=ORANGE, label="Opór liniowy")
axes[0].set_ylabel("Szybkość |v| [m/s]")
axes[0].set_title("Wartość prędkości", loc="left")
axes[0].legend(ncol=2)
axes[1].plot(t_drag, accel_d, color=PURPLE)
axes[1].set(xlabel="Czas t [s]", ylabel="Wartość przyspieszenia |a| [m/s²]")
axes[1].set_title("Przyspieszenie w modelu z oporem", loc="left")
fig.suptitle("Zmiana szybkości i przyspieszenia", fontweight="bold")
zapisz(fig, "szybkosc_przyspieszenie.png")
zapisz_svg("predkosci.svg", "Wartość prędkości", "Czas t [s]", "Szybkość |v| [m/s]", [
    (t_ideal, speed_i, "Bez oporu", BLUE), (t_drag, speed_d, "Opór liniowy", ORANGE)
])

# 5. Energie mechaniczne.
kin_i = 0.5 * m * (vx_i**2 + vy_i**2)
pot_i = m * g * y_i
kin_d = 0.5 * m * (vx_d**2 + vy_d**2)
pot_d = m * g * y_d
fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
ax.plot(t_ideal, kin_i + pot_i, color=BLUE, label="Suma energii, bez oporu")
ax.plot(t_drag, kin_d, color=ORANGE, label="Kinetyczna, opór liniowy")
ax.plot(t_drag, pot_d, color=GREEN, label="Potencjalna, opór liniowy")
ax.plot(t_drag, kin_d + pot_d, color=PURPLE, ls="--", label="Suma energii, opór liniowy")
ax.set(xlabel="Czas t [s]", ylabel="Energia [J]")
ax.set_title("Energia mechaniczna i praca siły oporu", loc="left")
ax.legend(fontsize=9, ncol=2)
zapisz(fig, "energia.png")
zapisz_svg("energia.svg", "Energia mechaniczna", "Czas t [s]", "Energia [J]", [
    (t_ideal, kin_i + pot_i, "Suma bez oporu", BLUE),
    (t_drag, kin_d, "Kinetyczna z oporem", ORANGE),
    (t_drag, pot_d, "Potencjalna z oporem", GREEN),
    (t_drag, kin_d + pot_d, "Suma z oporem", PURPLE),
])

# 6. Zasieg od kata: kazdy punkt ma osobno wyznaczony czas ladowania.
angles_deg = np.linspace(0.0, 90.0, 91)
ranges_ideal = v0**2 * np.sin(2.0 * np.deg2rad(angles_deg)) / g
ranges_drag = []
for angle_deg in angles_deg:
    angle = np.deg2rad(angle_deg)
    ranges_drag.append(pozycja_opor(czas_lotu_opor(angle), angle)[0])
fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
ax.plot(angles_deg, ranges_ideal, color=BLUE, label="Bez oporu")
ax.plot(angles_deg, ranges_drag, color=ORANGE, label="Opór liniowy")
ax.axvline(alpha_deg, color=INK, ls=":", lw=1.2, label="Rozpatrywany kąt 3°")
ax.set(xlabel="Kąt początkowy α [°]", ylabel="Zasięg [m]", xlim=(0, 90))
ax.set_title("Zasięg od kąta wyrzutu przy stałej szybkości początkowej", loc="left")
ax.legend()
zapisz(fig, "zasieg_kat.png")
zapisz_svg("zasieg_kat.svg", "Zasięg od kąta wyrzutu", "Kąt początkowy α [°]", "Zasięg [m]", [
    (angles_deg, ranges_ideal, "Bez oporu", BLUE),
    (angles_deg, ranges_drag, "Opór liniowy", ORANGE),
])

# Kontrole zgodnosci: warunki poczatkowe, ladowanie i bilans energii.
assert np.isclose(x_i[0], 0.0) and np.isclose(y_i[0], 0.0)
assert np.isclose(vx_i[0], v0 * np.cos(alpha))
assert abs(y_i[-1]) < 1e-10 and abs(y_d[-1]) < 1e-8
assert np.all(np.diff(kin_d + pot_d) <= 1e-10)

print(f"v0 = {v0:.2f} m/s; alpha = {alpha_deg:.1f} deg; g = {g:.2f} m/s^2")
print(f"m = {m:.3f} kg; b = {b:.3f} N s/m; gamma = {gamma:.6f} 1/s")
print(f"Bez oporu: czas lotu = {t_hit_ideal:.6f} s; zasieg = {zasięg_ideal:.6f} m; wysokosc max = {v0**2*np.sin(alpha)**2/(2*g):.6f} m")
print(f"Z oporem: czas lotu = {t_hit_drag:.6f} s; zasieg = {x_hit_drag:.6f} m; wysokosc max = {h_apex_drag:.6f} m; czas do szczytu = {t_apex_drag:.6f} s")
print(f"Maksymalny zasieg na siatce katow: {angles_deg[int(np.argmax(ranges_drag))]:.1f} deg")
print(f"Zapisano 6 wykresow w: {OUT}")
