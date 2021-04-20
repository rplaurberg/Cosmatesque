# Cosmatesque
Cosmatesque is a fractal-making program. It uses recurrence relations and modular arithmetic to generate arrays of integers which are then color-coded.

The user controls the parameters of the recurrence relation, modulus, and color-coding rules. The results are immediately reflected in a simplified preview on screen.  The user can save a high-resolution image of the pattern to their computer.

`Cosmateseque.py` contains the GUI and interactive elements.  The file `fractal.py` defines a class that handles the mathematical and image-making capacities.  The program requires `PySimpleGUIQt` for its GUI and `Pillow` and `numpy` for image generation.

By default images are saved with their parameters as a filename.  If you wish to explore beyond the constraints of the GUI (larger coefficient arrays, higher moduli) the `make_image` method in `fractal.py` allows picture generation using arbitrary parameters with the same textual format.

The GUI has been tested on one Windows PC (where it looks great) and one Mac (where it looks okay).  It has not yet been tested on a computer running Linux.

## What are recurrence relations?

A recurrence relation is a sequence of numbers in which the first few are specified and the rest are determined by a rule.  This program specifically looks at "path-counting" recurrence relations (my term) which have the following characteristics:

1. The number at the "origin" is 1.
2. All other numbers are determined by a rule that adds multiples of "nearby" numbers together in a specific way.
3. Numbers that are "out of bounds" are treated as zero.

This is perhaps best explained by examples.

### Example 1: The Fibonacci numbers

We'll look at the [Fibonacci numbers](https://en.wikipedia.org/wiki/Fibonacci_number) starting with 1.  The recurrence relation rule for the Fibonacci numbers states that each subsequent number is the sum of the previous two.  We start with 1.  For the next number there is only one previous number, namely 1, and the "the one before that" is in effect "out of bounds" so treated as 0.  Therefore the next entry is 0 + 1 = 1.  After that we have two previous numbers per new entry, so we can add both to come up with each new number: 1 + 1 = 2, then 1 + 2 = 3, then 2 + 3 = 5, and so on.  Here's what it looks like if we write these in a sequence:

>Fibonacci numbers: `1 1 2 3 5 8 13 21 34 55 ...`

The rule "each new number is the sum of the previous two" can be symbolized like so:

>Rule: `1 1 *`,

where the asterisk represents the number to be determined (the "cursor") and the numbers record the multiple of the previous entries to be added together.

### Variations on example 1

Let's look at some even simpler rules and how they generate other number sequences.

The rule 

>Rule: `1 *`,

"add the previous number" (to nothing else) produces a row of ones:

>Values: `1 1 1 1 1 1 1 1 1 1 ...`

The rule

>Rule: `2 *`,

"add twice the previous number" (to nothing else) produces powers of two:

>Values: `1 2 4 8 16 32 64 128 256 512 ...`

### Example 2: Pascal's triangle (in a square)

Now let's consider an example in two dimensions.  [Pascal's triangle](https://en.wikipedia.org/wiki/Pascal%27s_triangle) is usually presented as a triangular pattern of numbers, but we can rotate it slightly counterclockwise to put it in a square grid.  The famous recurrence relation for binomial coefficients (the entries of Pascal's triangle) translates into our square arrangement as the following rule.

```
Rule:
0 1
1 *
```

The values of Pascal's triangle in a 5x5 grid are shown below.

```
Values:
1  1  1  1  1
1  2  3  4  5
1  3  6 10 15
1  4 10 20 35
1  5 15 35 70 ...
```

### Example 3: The Delannoy Numbers

The [Delannoy numbers](https://en.wikipedia.org/wiki/Delannoy_number) are like our square version of Pascal's triangle with a diagonal added.  That is, we now use the following rule.

```
Rule:
1 1
1 *
```

Each new number is the sum of the number immediately to the left, the number immediately above, and the number immediately above and to the left.  The values of the Delannoy numbers in a 5x5 grid are shown next.

```
Values:
1   1   1   1   1
1   3   5   7   9
1   5  13  25  41
1   7  25  63 129
1   9  41 129 321 ...
```

## What is modular arithmetic?

[Modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic) is a way of taking integers and doing mathematics only with their remainders with respect to a *modulus*.  Even numbers have a remainder of zero with respect to 2 (they are "congruent to 0 modulo 2") and odd numbers have a remainder of 1 with respect to 2 (they are "congruent to 1 modulo 2").  For a given modulus *m*, the remainders 0 through *m*-1 are called the "residues" modulo *m*.

## What are fractals?

Fractals are geometrical shapes that are infinitely "gnarly," in that they possess interesting geometrical details at every scale as we zoom in.  Mathematically, a fractal can be described as a shape whose Hausdorff dimension exceeds its topological dimension.  Hausdorff dimension is a way of measuring how a shape occupies space from the "outside" in terms of covering sets.  Topological dimension is a way of describing how shapes take up space from the "inside" in terms of the number of parameters necessary to characterize their connected components.  For ordinary shapes (lines, circles, cubes, etc.) these two versions of "dimension" coincide.  But the infinite gnarly details of fractals gives them a higher Hausdorff dimension.  The *fract-* in "fractal" comes from "fractional dimension," meaning non-integer.

The Wikipedia gallery "[List of fractals by Hausdorff dimension](https://en.wikipedia.org/wiki/List_of_fractals_by_Hausdorff_dimension)" offers many illustrative examples.

## How do these ideas connect?

Let's start with a famous example.  If we color-code the entries of Pascal's triangle according to whether they are even or odd — that is, if we color-code their residues modulo 2 — then [the pattern that emerges](http://larryriddle.agnesscott.org/ifs/siertri/Pascal.htm) is an approximation of the fractal known as the [Sierpinski triangle](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_triangle).  The correspondence is exact at the "view from infinity," so to speak.  We can summarize this by saying the nonzero residues of Pascal's triangle modulo 2 generate the Sierpinski triangle.

For another example, the nonzero residues of the Delannoy numbers modulo 3 generate the [Sierpinski carpet](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_carpet), another famous fractal.

The connection is much deeper, however.  According to [this result of Pan](https://www.sciencedirect.com/science/article/pii/S0012365X0400322X), the nonzero residues moduly *any* prime of *any* recurrence relation with a rule encompassing a neighborhood of only adjacent values generate a fractal pattern.  In two dimensions, this includes Pascal's triangle, the Delannoy numbers, or *any* variation using other integer coefficients.  This also extends to any number of dimensions.

What if we look at moduli that are not primes?  Interestingly, [some results of Gamelin and Mnatsakanian](https://www.researchgate.net/publication/39676484_Arithmetic_based_fractals_associated_with_Pascal's_triangle) demonstrate that for Pascal's triangle, the fractal dimension of the pattern of nonzero residues modulo a power of a prime is exactly that of the fractal dimension of the pattern of nonzero residues modulo that prime raised only to the first power.  Even though the pattern becomes more complicated, the fractal dimension is some kind of invariant across powers of the prime.  Exploration of other patterns suggest this may be true for other recurrence relations as well. Research is ongoing.

## Why is this interesting?

These patterns establish fascinating connections between "local" phenomena — the values in these recurrence relations only "know" nearby numbers — and "global" phenomena, the resulting patterns of arbitrarily large scale.

Think of it this way.  Imagine you're with a bunch of people all playing cards on a wide-open space, something like the National Mall in Washington, D.C.  You're all in small clusters only interacting with those nearby, playing a very simple game with the same rules for everyone except for a single non-player in a far corner.  After a certain amount of time you're asked to stop and hold up the card in your hand.  A helicopter overhead takes an aerial shot of the upheld cards.  Despite a lack of planning on anyone's part, the upheld cards make a pixel-sharp picture as seen from the helicopter, spanning the entire field.

## Why did you call these "path-counting" recurrence relations?

The characteristics of path-counting recurrence relations listed above — start with a 1, have a fixed set of rules, and ignore out-of-bound references — mean that the resulting grids of numbers count the number of paths from the origin to each square using moves described by the rule grid.  This is more apparent if we flip the rule grids.

Recall the rule for the Fibonacci numbers:

>Rule: `1 1 *`

Flip the rule and call it "moves":

>Moves: `* 1 1`

Intepret this as "you can move one space forward (only one way) or two spaces forward (only one way)."  Imagine we have a chess piece that can move either one space forward or two spaces forward.  Then the Fibonacci numbers count the number of ways this chess piece can get from the origin to each square:

>Fibonacci numbers: `1 1 2 3 5 8 13 21 34 55 ...`

Interpret the first 1 at the origin to be the empty path from the origin to itself, consisting of no moves at all.  There is only one way to make no moves at all, so that makes sense.  For the next number, there is only path going from the origin to that first square: move one square right once.  For the square after that, we can either get there by moving one square right twice or two moves right once, hence the number is 2.  And so on.

Recall our powers-of-two example earlier, arising from the following rule.

>Rule: `2 *`

Flip that to turn it into a move set:

>Moves: `* 2`

We can interpret this as signifying two possible ways to move from each square to the square immediately to the right.  This can mean two differently colored paths, if we're talking paths, or perhaps two different flourishes if we're imagining chess pieces.  The number of ways of combining these colors/flourishes doubles as we proceed:

>Values: `1 2 4 8 16 32 64 128 256 512 ...`

Similar path-counting interpretations apply to the two-dimensional patterns.

The chess-piece interpretation lends itself to one of the most beguiling titles of a math paper I've come across, "[King's walk on the infinite chessboard](https://www.semanticscholar.org/paper/King%27s-walk-on-the-infinite-chessboard-Sved-Clarke/e223a6543131e8f0670c54823c4eec2cef98f245)."

## What does Cosmatesque mean?

"Cosmatesque" refers to a type of [medieval mosaic](https://www.researchgate.net/publication/259341701_SIERPINSKY_TRIANGLES_IN_STONE_ON_MEDIEVAL_FLOORS_IN_ROME), some of which included depictions of what we would later call the Sierpinski triangle.  The pictures this program generates can be considered mosaics of pixels.

## What's this gradient stuff?

Each gradient image comes from combining copies of the matching black-and-white image at several zoom levels, using the modulus as a zoom factor.  There is no mathematical significance to this that I know of, but the resulting images have a distinct aesthetic appeal.

## What is Fredkin's replicator?

Fredkin's replicator is a kind of [cellular automaton](https://oeis.org/A160239), stages of which appear as the nonzero residues of one particular recurrence relation.
