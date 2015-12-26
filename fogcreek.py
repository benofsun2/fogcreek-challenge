#!/usr/bin/env python
# -*- coding: utf8 -*-

"""My solution to a challenge by Fogcreek."""

from __future__ import print_function

import argparse


VERBOSE = False


def trim_after_underscore(s):
    """Return the characters before the underscore."""
    return s.split('_')[0]


def widest_leftmost_pair(s):
    """Return the indices of the widest, leftmost pair, or None.

    This is the core of the algorithm. We call 'pair' two equal characters with
    no equal characters between them.

    We mantain two indices, i and j, which are pointing respectively to the
    start and the end of the current candidate pair. We also mantain a
    dictionary of the characters seen for the current i, and the first
    character pointed by i.

    In the following 'x' and 'y' are specific characters, '_' are characters
    with no repeated characters among them and '?' is an unspecified character.

    We have three cases:

      1. We have just seen a character that is equal to the first character.
         In our notation:

         x_?___x
         i k   j

         We now have two subcases:

           a) We have seen that character between i and j:

              x_x___x
              i k   j

              We found a pair, so we add (i, j) to the list of pairs. We also
              found (k, j), but we already know that the former is both wider
              and to the left of the latter. We can now advance i to k, since
              we already know that between i and j there are no repeated
              characters apart from x.

           b) We didn't:

              x_____x
              i     j

              We found a pair, so we add (i, j) to the list of pairs. But i
              could still be part of another pair as in case 1a, so we update
              the seen dictionary and we increment j.

      2. We have just seen a character that we've already seen between i and j,
         different from the first character:

         x_y___y
         i k   j

         We found a pair, so we add (k, j) to the list of pairs. We can now
         advance i to k, since we already know that between i and j there are
         no repeated characters apart from y.

      3. We have not yet found a pair of equal characters:

         x______
         i     j

         So we just add the character at j to the seen characters and we
         increment j.
    """
    pairs = []
    seen = {}
    first = s[0]
    i, j, l = 0, 1, len(s)

    if VERBOSE:
        print(s)

    while i < l and j < l:
        if s[j] == first:
            # Case 1: x_?___x
            #         i     j
            if s[j] in seen:
                # Case 1a: x_x___x
                #          i k   j
                pairs.append((i, j))

                i = seen[s[j]]
                j = i + 1

                seen = {}
                first = s[i]
            else:
                # Case 1b: x_____x
                #          i     j
                pairs.append((i, j))

                seen[s[j]] = j
                j += 1
        elif s[j] in seen:
            # Case 2: x_y___y
            #         i k   j
            pairs.append((seen[s[j]], j))

            i = seen[s[j]]
            j = i + 1

            seen = {}
            first = s[i]
        else:
            # Case 3: x______
            #         i     j
            seen[s[j]] = j
            j += 1

    try:
        return max(pairs, key=lambda el: (el[1] - el[0], l - el[0]))
    except ValueError:
        return None


def update_string(s, pair):
    """Delete a pair of equal characters and append one of them at the end."""
    return s[:pair[0]] + s[pair[0]+1:pair[1]] + s[pair[1]+1:] + s[pair[1]]


def solve(s):
    """Keep removing pairs until they are depleted, then trim after the '_'."""
    pair = widest_leftmost_pair(s)
    while pair:
        s = update_string(s, pair)
        pair = widest_leftmost_pair(s)

    return trim_after_underscore(s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file', help='file to be processed')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show each step of the algorithm')

    args = parser.parse_args()

    f = open(args.input_file, 'r')
    s = ''.join(f.read().splitlines())
    VERBOSE = args.verbose

    print(solve(s))
