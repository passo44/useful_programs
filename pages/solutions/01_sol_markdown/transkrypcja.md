# Transkrypcja

![Zrzut ekranu notatek](zrzut.png)

## Prompt użyty do wygenerowania tekstu przez AI

```text
Przepisz odręczne notatki ze zrzutu ekranu do czystego kodu Markdown. 
Zwróć szczególną uwagę na poprawne zakodowanie wzorów matematycznych w formacie LaTeX.
Dla wzorów wewnątrz linii użyj pojedynczych znaków dolara (\(...\)), pamiętając o dodaniu spacji przed pierwszym dolarem, aby GitHub poprawnie zainicjował tryb matematyczny.
Dla dużych, samodzielnych równań użyj bloków display math (\[...\]) wydzielonych w osobnych liniach, pozostawiając pustą linię nad i pod blokiem.
Wszystkie punkty odręczne zamień na czytelną listę punktowaną w Markdown.
```

## Finalna wersja notatki

### 11. CO TO SĄ KROPKI KWANTOWE I JAKIE MAJĄ WŁASNOŚCI?

- **0D** struktura
- ruch elektronu ograniczony w trzech wymiarach
- najprostszy model – *quantum box* – kropka kwantowa w kształcie sześcianu, na zewnątrz potencjał nieskończony
- równanie Schrödinger'a:

$$
-\frac{\hbar^2}{2m} \left( \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + \frac{\partial^2}{\partial z^2} \right) \Psi(x,y,z) = E\Psi(x,y,z)
$$

- energia:

$$
E = \frac{\hbar^2 \pi^2}{2m} \left( \frac{n_x^2}{L_x^2} + \frac{n_y^2}{L_y^2} + \frac{n_z^2}{L_z^2} \right)
$$

- stany energetyczne są zdegenerowane
- sferyczna kropka kwantowa $\implies$ rozłożenie funkcji falowej $\Psi$ na część radialną i kątową (podobieństwo do zagadnienia atomu wodoru w mechanice kwantowej)
- $\implies$ rozwiązanie – funkcje Bessela typu $J_{l+1/2}$

### 12. PORÓWNAĆ WŁASNOŚCI HETEROSTRUKTUR, DRUTÓW I KROPKOWYCH KWANTOWYCH.

