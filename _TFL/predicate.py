# -*- coding: iso-8859-15 -*-
# Copyright (C) 1998-2012 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.predicate
#
# Purpose
#    Provide predicate-functions for iterables
#
# Revision Dates
#    19-Mar-1998 (CT) Creation
#     4-Apr-1998 (CT) `paired' renamed to `pairwise'
#                     `paired' added
#    26-Apr-1998 (CT) `paired'   implemented via `map' instead of `for'-loop
#    26-May-1998 (CT) `pairwise' implemented via `map' instead of `for'-loop
#    26-May-1998 (CT) `cartesian' added
#     3-Jun-1998 (CT) `xored_string' added
#    10-Jul-1998 (CT) `reversed'     added
#    28-Jan-1999 (CT) `split_by_key' added
#    28-Jan-1999 (CT) `intersection' defined here (was in `Math_Func.py')
#    19-Feb-1999 (CT) `matches'      added
#    22-Feb-1999 (CT) `common_head'  added
#    26-Feb-1999 (CT) `matches' renamed to `re_matches', `matches' added
#    13-Aug-1999 (CT) `bit_size_cmp' added
#    29-Oct-1999 (CT) `identity' and `cross_sum' added
#    23-Nov-1999 (CT) `random_string' added
#    27-Jan-2000 (CT) `extender' added and `flattened' optimized by map-ping it
#    10-Mar-2000 (CT) `relax' added
#    14-Mar-2000 (CT) `un_nested' added
#    24-Mar-2000 (CT) `flattened' uses `un_nested'
#    27-Mar-2000 (CT) `cartesian' changed to call `flattened' directly
#                     (using `apply' fails if a one-element list is passed
#                     into `flattened' -- `un_nested' then does too much of a
#                     good thing)
#     5-Apr-2000 (CT) Optional parameter `min_result_size' added to
#                     `split_by_key'
#    11-Apr-2000 (CT) `split_by_key' corrected (handle empty `seq' gracefully)
#     9-May-2000 (CT) `head_slices' added
#    30-May-2000 (CT) `byte_alignment' added
#    30-May-2000 (CT) `bit_size_cmp' tentatively changed to cmp regarding
#                     `byte_alignment'
#     8-Nov-2000 (CT) `has_substr' added
#     9-Jan-2001 (CT) Use `operator.add' instead of hone grown lambda
#     9-Jan-2001 (CT) `Indices' and `IV_Pairs' added
#     7-Mar-2001 (CT) Comment added to `relax'
#    20-Sep-2001 (AGO) `union' added
#    17-Dec-2001 (CT)  `extender` changed to apply `list`
#    11-Mar-2002 (CT)  `list_difference` added
#     4-Jul-2002 (CT)  `bit_alignment` added
#    29-Jul-2002 (CT)  `dsu_ed` added
#    29-Jul-2002 (CT)  `_predicate_22` and `_predicate_21` factored to be able
#                      to use generators where available
#     1-Aug-2002 (CT)  s/dsu_ed/dusort/g
#    29-Aug-2002 (CT)  `bit_size_decorator` added
#    06-Sep-2002 (RMA) Moved pairwise from '_predicate_21' because change
#                      from 29-Jul does not work for pairwise.
#    13-Dec-2002 (CT)  `intersection_n` and `intersection_ns` added
#    14-Jan-2003 (CT)  `first` added
#     4-Feb-2003 (CT)  `sorted` argument added to `split_by_key`
#     4-Feb-2003 (CT)  `dusplit_by_key` added
#     5-Feb-2003 (CED) `dusplit_by_key` removed
#    11-Mar-2003 (CT)  `second` added
#    19-Mar-2003 (CED) `lists_equal` added
#     9-Apr-2003 (CT)  `dict_from_list` used
#    13-May-2003 (CED) `tupelize` added
#     5-Jun-2003 (CT)  `third` added
#     6-Jun-2003 (CT)  `sum` added if not there already (2.3 adds a builtin
#                      for this)
#    17-Jun-2003 (CED) `gcd`, `gcd_n`, `lcm`, `lcm_n` added
#     1-Jul-2003 (CED) `lcm_n` fixed
#     1-Aug-2003 (CT)  `rounded_up` and `rounded_down` added
#    13-Aug-2003 (CED) 'rounded_up` fixed
#    18-Aug-2003 (CT)  `pairwise` changed to use `zip` instead of `map`
#    29-Aug-2003 (CT)  Optional argument `sorted` removed from `split_by_key`
#    29-Aug-2003 (CT)  `dusplit` added
#    26-Oct-2003 (CT)  `all_true` and `any_true` added
#    26-Oct-2003 (CT)  `all_true_p` and `any_true_p` added
#    26-Oct-2003 (CT)  Ancient and obsolete `number_q`, `forall_q`, and
#                      `exists_q`
#    21-Nov-2003 (CT)  Stupid typo in `any_true` fixed
#    12-Dec-2003 (CT)  References to modules `string` and `types` removed
#    19-Feb-2004 (CED) `rotate_l/r` added
#     1-Apr-2004 (CT)  `apply` removed
#     1-Apr-2004 (CT)  `split_by_key`, `dusplit` and `common_head` changed to
#                      work with generators, too
#     1-Apr-2004 (CT)  Some doc-tests added
#     1-Apr-2004 (CT)  `flatten` added (didn't dare to remove `flattened`
#                      although that one dies if called with a single flat
#                      sequence as argument)
#     1-Apr-2004 (CT)  `cartesian` simplified by using list comprehension
#                      instead of `map`
#     2-Apr-2004 (CT)  Yesterday's `apply` removal reverted
#                      (sorry for the stupid breakage!)
#     2-Apr-2004 (CT)  `cartesian` changed to use `flattened` again
#    10-May-2004 (CED) `pairwise_circle` added
#    11-May-2004 (CED) `is_contiguous` added
#    25-May-2004 (CED) Some doctests added
#    30-Jun-2004 (CT)  `list_difference` fixed to do what the doc-string
#                      claims it does
#    20-Oct-2004 (CED) Some doctests added, some `map` calls replaced by
#                      list comprehension
#    20-Oct-2004 (CED) `list` used where possible
#    15-Nov-2004 (CED) Second parameter of `dusort`, `dusplit` made optional
#    24-Mar-2005 (CT)  Moved into package `TFL` and removed
#                      various cruft
#     3-Apr-2005 (CT)  Use built-in `reversed` and `sorted` if any instead of
#                      defining home-grown versions
#     3-Apr-2005 (CT)  Base `dusort` on built-in `sorted` if available
#     7-Apr-2005 (CED) `is_contiguous` made more robust
#     8-Jun-2005 (CT)  Home-grown `sorted` and `dusort` factored
#                      to `_sorted` and `_dusort` and made
#                      API-compatible to Python-2.4's builtin
#                      `sorted` and `dusort`
#    16-Jun-2005 (CT)  `list_difference` changed to use `set`
#     1-Jul-2005 (CT)  Renamed `first`, `second`, `third` by
#                      `first_arg`, `second_arg`, `third_arg`
#     1-Jul-2005 (CT)  `first` added
#     1-Jul-2005 (CT)  `predecessor_of` and `successor_of` added
#     1-Jul-2005 (CT)  `pairwise_circle` moved to `Generators`
#    13-Jul-2005 (CED) `lists_equal` changed to use sets, `intersection_n`
#                      changed to use generator instead of list-comprehension
#    19-Jul-2005 (CT)  `union` changed to use `set`
#    19-Jul-2005 (CT)  `union` streamlined (thanks for pointing out the
#                      braino, CED)
#    19-Jul-2005 (CT)  Style improvements
#    19-Jul-2005 (CT)  Historical ballast removed (`map`, `apply`)
#    30-Aug-2005 (CT)  `split_hst` and `rsplit_hst` added
#    30-Aug-2005 (CT)  Use `in` instead of `find`
#    31-Aug-2005 (CT)  `rsplit_hst` changed to match Hettinger's clarification
#     9-Feb-2006 (CT)  `bool_split` added
#    28-Feb-2006 (CT)  `pairs_1w` and `pairs_2w` added
#     9-May-2006 (CT)  `bit_size_cmp` removed (long since stale)
#     6-Sep-2006 (CT)  Doc-strings of `split_hst` and `rsplit_hst` corrected
#     8-Dec-2006 (CT)  `window_wise` made visible
#    16-Feb-2007 (CT)  `enumerate_slice` made visible
#     2-Aug-2007 (CED) `is_ordered`, `rotated_until_ordered` added
#    14-Aug-2007 (CED) `is_ordered` simplified, `unified` added
#    20-Aug-2007 (CED) s/unified/uniq/
#    13-Nov-2007 (CT)  `rounded_to` added
#    23-Jan-2009 (CT)  `filtered_join` added
#    23-Jan-2009 (CT)  Broken `rotated_until_ordered` removed,
#                      `is_ordered` de-obfuscated (removed criminal energy,
#                      indeed)
#    24-Sep-2009 (CT)  `callable` added
#     3-Nov-2009 (CT)  Use `TFL.paired_map` instead of built-in map (which
#                      will change semantics in 3.x)
#    11-Nov-2009 (CT)  Legacy `_sorted` changed to 3-compatibility
#    13-Nov-2009 (CT)  `tupled` removed (Usage of `map` is not compatible with
#                      Python 3.x)
#     2-Dec-2009 (CT)  `uniq_p` added
#     2-Dec-2009 (CT)  `intersection`, `intersection_n` and `union` modernized
#     2-Dec-2009 (CT)  `_sorted` removed (only needed for ancient Pythons)
#     1-Jan-2010 (CT)  `first_diff` added
#     2-Jun-2010 (CT)  `undotted_dict` added
#    30-Jun-2010 (CT)  `sliced` added
#     8-Sep-2010 (MG)  `dotted_dict` added
#     9-Oct-2010 (MG)  `undotted_dict`and `dotted_dict`: Parameter `sep` added
#     8-Sep-2011 (CT)  `first_n` added
#    12-Sep-2012 (CT)  Use `itertools.product` for `cartesian`, if available
#    ��revision-date�����
#--

from   _TFL             import TFL

import _TFL.Generators

import itertools

### legacy aliases
IV_Pairs        = enumerate
dict_from_list  = dict.fromkeys
enumerate_slice = TFL.enumerate_slice
pairwise        = TFL.pairwise
window_wise     = TFL.window_wise

def all_true (seq) :
    """Returns True if all elements of `seq` are true,
       otherwise returns first non-true element.
    """
    for e in seq :
        if not e :
            return e
    else :
        return True
# end def all_true

def all_true_p (seq, pred) :
    """Returns True if `pred` returns true for all elements of `seq`,
       otherwise returns first non-true element.
    """
    for e in seq :
        if not pred (e) :
            return e
    else :
        return True
# end def all_true_p

def any_true (seq) :
    """Returns first true element of `seq`, otherwise returns False."""
    for e in seq :
        if e :
            return e
    else :
        return False
# end def any_true

def any_true_p (seq, pred) :
    """Returns first element of `seq` for which `pred` returns True,
       otherwise returns False.
    """
    for e in seq :
        if pred (e) :
            return e
    else :
        return False
# end def any_true_p

def bit_alignment (bits) :
    """Returns alignment in powers of two of data with length `bits'

       >>> [(i, bit_alignment (i)) for i in range (0, 9)]
       [(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)]
       >>> [(i, bit_alignment (i)) for i in range (8, 33, 4)]
       [(8, 1), (12, 2), (16, 2), (20, 1), (24, 1), (28, 4), (32, 4)]
    """
    return byte_alignment ((bits + 4) >> 3)
# end def bit_alignment

def bit_size_decorator (bs) :
    """Return a decorator for `dusort`-ing by bit-size `bs`.

       Integral byte sizes compare before sub-byte sizes, even sizes compare
       before odd sizes, larger values compare before smaller values.
    """
    return - byte_alignment ((bs + 4) >> 3), - bs
# end def bit_size_decorator

def bool_split (seq, predicate) :
    """Returns two lists, the first containing all elements of
       `seq` for which `predicate` evaluates to false, the second
       all others.

       >>> bool_split (range (10), lambda x : x % 2)
       ([0, 2, 4, 6, 8], [1, 3, 5, 7, 9])
       >>> bool_split (range (10), lambda x : x > 5)
       ([0, 1, 2, 3, 4, 5], [6, 7, 8, 9])
       >>> bool_split (range (5), lambda x : x < 5)
       ([], [0, 1, 2, 3, 4])
       >>> bool_split (range (5), lambda x : x > 4)
       ([0, 1, 2, 3, 4], [])
    """
    result = ([], [])
    add    = [r.append for r in result]
    for e in seq :
        add [bool (predicate (e))] (e)
    return result
# end def bool_split

def byte_alignment (bytes) :
    """Returns alignment in powers of two of data with length `bytes'

       >>> [(i, byte_alignment (i)) for i in range (-3, 3)]
       [(-3, 1), (-2, 2), (-1, 1), (0, 0), (1, 1), (2, 2)]
       >>> [(i, byte_alignment (i)) for i in range (3, 10)]
       [(3, 1), (4, 4), (5, 1), (6, 2), (7, 1), (8, 8), (9, 1)]
    """
    return (bytes ^ (bytes - 1)) & bytes
# end def byte_alignment

def callable (obj) :
    """Return whether the object is callable (i.e., some kind of function).
       Note that classes are callable, as are instances with a __call__()
       method.
    """
    return hasattr (obj, "__call__")
# end def callable

try :
    itertools.product
except AttributeError :
    def cartesian (s1, s2, combiner = None) :
        """Returns the cartesian product of the sequences `s1' and `s2'.

           >>> l = (3, 1, 7)
           >>> cartesian (l, l)
           [(3, 3), (3, 1), (3, 7), (1, 3), (1, 1), (1, 7), (7, 3), (7, 1), (7, 7)]
        """
        if combiner is None :
            combiner = paired
        result = [combiner ((x, ) * len (s2), s2) for x in s1]
        return flattened (result)
    # end def cartesian

    def cartesian_n (s1, s2, * si) :
        """Returns the cartesian product of all the sequences given.

           >>> l = (3, 1, 7)
           >>> cartesian_n (l, l)
           [(3, 3), (3, 1), (3, 7), (1, 3), (1, 1), (1, 7), (7, 3), (7, 1), (7, 7)]
           >>> l = (3, 1)
           >>> cartesian_n (l, l, l)
           [(3, 3, 3), (3, 3, 1), (3, 1, 3), (3, 1, 1), (1, 3, 3), (1, 3, 1), (1, 1, 3), (1, 1, 1)]
        """
        result = cartesian (s1, s2)
        for s in si :
            result = cartesian \
                ( result, s
                , lambda a, b : map (lambda l, r : l + (r, ), a, b)
                )
        return result
    # end def cartesian_n
else :
    def cartesian (* iterables) :
        """Cartesian product of `iterables`.

           >>> l = (3, 1, 7)
           >>> cartesian (l)
           [(3,), (1,), (7,)]

           >>> cartesian (l, l)
           [(3, 3), (3, 1), (3, 7), (1, 3), (1, 1), (1, 7), (7, 3), (7, 1), (7, 7)]

           >>> cartesian_n ((1,2), ("a", "b"))
           [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]

           >>> cartesian ((1,2), ("a", "b"), ("x", "y"))
           [(1, 'a', 'x'), (1, 'a', 'y'), (1, 'b', 'x'), (1, 'b', 'y'), (2, 'a', 'x'), (2, 'a', 'y'), (2, 'b', 'x'), (2, 'b', 'y')]

        """
        return list (itertools.product (* iterables))
    # end def cartesian

    cartesian_n = cartesian

def common_head (list) :
    """Return common head of all strings in `list'.
       >>> common_head ([])
       ''
       >>> common_head (["a"])
       'a'
       >>> common_head (["a", "b"])
       ''
       >>> common_head (["ab", "ac", "b"])
       ''
       >>> common_head (["ab", "ac", "ab"])
       'a'
       >>> common_head (["abc", "abcde", "abcdxy"])
       'abc'
    """
    result = ""
    list   = sorted (list)
    if list :
        match = [(l == r and r) or "\0"
                for (l, r) in zip (list [0], list [-1])
                ]
        try :
            last = match.index ("\0")
        except ValueError :
            last = len (match)
        result = "".join (match [:last])
    return result
# end def common_head

def cross_sum (seq, fct = None) :
    """Returns the sum over all elements of `seq' passed trough `fct'.

       `fct' must be a function taking one argument and returning something
       that can be added.
    """
    if fct is None :
        fct = identity
    return sum (fct (x) for x in seq)
# end def cross_sum

def _dusort (seq, decorator, reverse = False) :
    """Returns a sorted copy of `seq`. The sorting is done over a
       decoration of the form `decorator (p), i, p for (i, p) in
       enumerate (seq)`.

       >>> _dusort ([1, 3, 5, 2, 4], lambda e : -e)
       [5, 4, 3, 2, 1]
    """
    temp = [(decorator (p), i, p) for (i, p) in enumerate (seq)]
    temp.sort ()
    result = [p [-1] for p in temp]
    if reverse :
        result.reverse ()
    return result
# end def _dusort

try :
    sorted
except NameError :
    dusort = _dusort
else :
    def dusort (seq, decorator, reverse = False) :
        """Wrapper around built-in sorted that is backwards compatible to
           home-grown `dusort`

           >>> dusort ([1, 3, 5, 2, 4], lambda e : -e)
           [5, 4, 3, 2, 1]
           >>> dusort ([1, 3, 5, 2, 4], lambda e : e, reverse = True)
           [5, 4, 3, 2, 1]
        """
        return sorted (seq, key = decorator, reverse = reverse)
    # end def dusort

def dusplit (seq, decorator, min_result_size = 1) :
    """Returns a list of lists each containing the elements of `seq'
       comparing equal under `decorator` (`dusplit` is to `split_by_key` what
       `dusort` is to `sorted`).

       >>> dusplit ([(0,1), (1,1), (0,2), (0,3), (2,3)], lambda x : x [0])
       [[(0, 1), (0, 2), (0, 3)], [(1, 1)], [(2, 3)]]
       >>> dusplit ([(0,1), (1,1), (0,2), (0,3), (2,3)], lambda x : x [1])
       [[(0, 1), (1, 1)], [(0, 2)], [(0, 3), (2, 3)]]
    """
    result = [[]]
    temp   = [(decorator (p), i, p) for (i, p) in enumerate (seq)]
    if temp :
        temp.sort ()
        for (a, b) in TFL.pairwise (temp) :
            result [-1].append (a [-1])
            if a [0] != b [0] :
                result.append ([])
        result [-1].append (temp [-1] [-1])
    if len (result) < min_result_size :
        result = result + ([[]] * (min_result_size - len (result)))
    return result
# end def dusplit

def extender (l, tail) :
    """Return list `l' extended by `tail' (`l' is changed in place!)

       >>> extender ([1, 2, 3], (4, 5))
       [1, 2, 3, 4, 5]
       >>> extender ([], [1])
       [1]
    """
    l.extend (tail)
    return l
# end def extender

def filtered_join (sep, strings, pred = None) :
    """Return a string which is the concatenation of the items in the
       iterable `strings` for which `pred` is true, separated by `sep`.

       >>> filtered_join ("-", ["", "abc", "ced"])
       'abc-ced'
       >>> filtered_join ("-", [" ", "abc", "ced"])
       ' -abc-ced'
    """
    if pred is None :
        import operator
        pred = operator.truth
    return sep.join (s for s in strings if pred (s))
# end def filtered_join

def first (iterable) :
    """Return first element of iterable"""
    try :
        return iter (iterable).next ()
    except StopIteration :
        raise IndexError
# end def first

def first_arg (x, * args, ** kw) :
    """Returns the first argument unchanged"""
    return x
# end def first_arg

def first_diff (a, b) :
    """Return index of first difference in iterables `a` and `b`.

       >>> first_diff ("a", "b")
       0
       >>> first_diff ("a", "a")
       1
       >>> first_diff ("a", "ab")
       1
       >>> first_diff ("ac", "ab")
       1
       >>> first_diff ("abc", "ab")
       2
       >>> first_diff ("abcdef", "ab")
       2
       >>> first_diff ("abcdefgh", "abcDefgh")
       3
       >>> "abcdefgh"[3], "abcDefgh"[3]
       ('d', 'D')
    """
    i = -1
    for i, (l, r) in enumerate (paired (a, b)) :
        if l != r :
            return i
    return i + 1
# end def first_diff

def first_n (iterable, n, default = None) :
    """Generate first n elements of iterable, filling with `default` if
       necessary.

       >>> it = (1,2,3)
       >>> for n in range (6) :
       ...   print n, tuple (first_n (it, n))
       ...
       0 ()
       1 (1,)
       2 (1, 2)
       3 (1, 2, 3)
       4 (1, 2, 3, None)
       5 (1, 2, 3, None, None)
    """
    for i, x in enumerate (iterable) :
        if i >= n :
            break
        yield x
    for k in range (i+1, n) :
        yield default
# end def first

def flatten (* lists) :
    """Returns a list containing all the elements in `lists'.

       >>> flatten (range (3))
       [0, 1, 2]
       >>> flatten (range (3), range (2))
       [0, 1, 2, 0, 1]
       >>> flatten ((range (3), range (2)))
       [[0, 1, 2], [0, 1]]
    """
    result = []
    for l in lists :
        result.extend (un_nested (l))
    return result
# end def flatten

def flattened (* lists) :
    """Returns a list containing all the elements in `lists'.

       >>> flattened (range (3), range (2))
       [0, 1, 2, 0, 1]
       >>> flattened ((range (3), range (2)))
       [0, 1, 2, 0, 1]
    """
    result = []
    for l in un_nested (lists) :
        extender (result, l)
    return result
# end def flattened

def has_substr (s, subs) :
    """Returns true if `s' contains `subs'"""
    return subs in s
# end def has_substr

def head_slices (l) :
    """Returns the list of all slices anchored at head of `l'

       >>> head_slices ("abcdef")
       ['a', 'ab', 'abc', 'abcd', 'abcde', 'abcdef']
    """
    return [l [:i] for i in range (1, len (l) + 1)]
# end def head_slices

def identity (x) :
    """Returns its argument unchanged"""
    return x
# end def identity

def intersection (l, r) :
    """Compute intersection of lists `l' and `r'.

       >>> intersection (range (4), range (2,5))
       [2, 3]
    """
    r_set = set (r)
    return [x for x in l if x in r_set]
# end def intersection

def intersection_n (l1, * ls) :
    """Compute intersection of `l1` and all elements of `ls`."""
    result = set (l1)
    for l in ls :
        result.intersection_update (l)
    return result
# end def intersection_n

def intersection_ns (lists) :
    return intersection_n (* lists)
# end def intersection_ns

def is_contiguous (seq) :
    """Tells whether the sequence of integers in `seq` is contiguous

       >>> is_contiguous ([1, 2, 3, 4, 5])
       True
       >>> is_contiguous ([10, 8, 9])
       True
       >>> is_contiguous ([42])
       True
       >>> is_contiguous ([])
       True
       >>> is_contiguous ([1, 3, 4])
       False
    """
    for l, r in TFL.pairwise (sorted (seq)) :
        try :
            if (r - l) != 1 :
                return False
        except TypeError :
            return False
    return True
# end def is_contiguous

def is_ordered (seq, decorator = None) :
    """Returns whether `seq` is ordered (according to `decorator`)

       >>> from _TFL.Accessor import Getter
       >>> is_ordered ([0, 1, 3, 7])
       True
       >>> is_ordered ([0, 1, 4, 3])
       False
       >>> is_ordered ([0, 0, 1, 1])
       True
       >>> is_ordered ([1])
       True
       >>> is_ordered ([])
       True
       >>> is_ordered ([(2, 0), (1, 1), (3, 2)], Getter [0])
       False
       >>> is_ordered ([(2, 0), (1, 1), (3, 2)], Getter [1])
       True
    """

    if decorator is not None :
        seq = (decorator (e) for e in seq)
    return all_true (l <= r for l, r in pairwise (seq))
# end is_ordered

def list_difference (l, r) :
    """Compute difference of `l` and `r`.

       >>> range (3), range (2,5)
       ([0, 1, 2], [2, 3, 4])
       >>> list_difference (range (3), range (2, 5))
       [0, 1]
       >>> list_difference (range (10), range (3))
       [3, 4, 5, 6, 7, 8, 9]
    """
    rs = set (r)
    return [y for y in l if y not in rs]
# end def list_difference

def lists_equal (l, r) :
    """True if set of elements of `l` and `r` is equal.

       >>> l = range (3)
       >>> r = l[::-1]
       >>> l,r
       ([0, 1, 2], [2, 1, 0])
       >>> lists_equal (l, r)
       True
    """
    return set (l) == set (r)
# end def lists_equal

def matches (list, txt, prefix = "^") :
    """Returns all strings in `list' starting with `txt'.

       If you pass an empty string for `prefix', `matches' returns all
       elements containing `txt'.
    """
    import re
    return re_matches (list, re.compile (prefix + re.escape (txt)))
# end def matches

def paired (s1, s2) :
    """Returns a list of pairs
       `((s1 [0], s2 [0]), ... (s1 [n-1], s2 [n-1]))'.

       >>> paired ([1, 2, 3], [1, 2, 3])
       [(1, 1), (2, 2), (3, 3)]
       >>> paired ([1, 2, 3], [1])
       [(1, 1), (2, None), (3, None)]
       >>> paired ([1], [1, 2, 3])
       [(1, 1), (None, 2), (None, 3)]
       >>> paired ([], [])
       []
    """
    return list (TFL.paired_map (s1, s2))
# end def paired

def pairs_1w (seq) :
    """Generates all pairs (one-way) in `seq` which must allow
       repeated iteration (i.e., cannot be a generator).

       >>> ["".join (p) for p in pairs_1w ("abcd")]
       ['ab', 'ac', 'ad', 'bc', 'bd', 'cd']
       >>> list (pairs_1w ("abc"))
       [('a', 'b'), ('a', 'c'), ('b', 'c')]
       >>> list (pairs_1w ("ab"))
       [('a', 'b')]
       >>> list (pairs_1w ("a"))
       []
       >>> list (pairs_1w (""))
       []
    """
    for i, a in enumerate (seq [:-1]) :
        for b in seq [i+1:] :
            yield a, b
# end def pairs_1w

def pairs_2w (seq) :
    """Generates all pairs (two-way) in `seq` which must allow
       repeated iteration (i.e., cannot be a generator).

       >>> ["".join (p) for p in pairs_2w ("abcd")]
       ['ab', 'ba', 'ac', 'ca', 'ad', 'da', 'bc', 'cb', 'bd', 'db', 'cd', 'dc']
       >>> ["".join (p) for p in pairs_2w ("abc")]
       ['ab', 'ba', 'ac', 'ca', 'bc', 'cb']
       >>> ["".join (p) for p in pairs_2w ("ab")]
       ['ab', 'ba']
       >>> ["".join (p) for p in pairs_2w ("a")]
       []
       >>> ["".join (p) for p in pairs_2w ("")]
       []
    """
    for a, b in pairs_1w (seq) :
        yield a, b
        yield b, a
# end def pairs_2w

def predecessor_of (element, iterable, pairwise = pairwise) :
    """Returns the predecessor of `element` in `iterable`"""
    for (l, r) in pairwise (iterable) :
        if r == element :
            return l
    raise IndexError
# end def predecessor_of

def random_string (length, char_range = 127, char_offset = 128) :
    """Returns a string of `length' random characters in the interval
       (`char_offset', `char_offset + char_range').
    """
    from random import random
    return "".join \
        (   chr (int (random () * char_range + char_offset))
        for c in range (length)
        )
# end def random_string

def relax (* args, ** kw) :
    """Dismisses its arguments"""
    pass
# end def relax

def reversed_list (seq) :
    """Returns a reversed copy of `seq'.

       >>> reversed_list ([1, 2, 3, 4, 5])
       [5, 4, 3, 2, 1]
       >>> reversed_list ([1])
       [1]
       >>> reversed_list ([])
       []
    """
    result = list (seq)
    result.reverse ()
    return result
# end def reversed_list

try :
    reversed = reversed
except NameError :
    reversed = reversed_list

def re_matches (list, pat) :
    """Returns all strings in `list' matching the regular expression `pat'."""
    if isinstance (pat, (str, unicode)) :
        import re
        pat = re.compile (pat)
    return \
        [s for s in list if isinstance (s, (str, unicode)) and pat.search (s)]
# end def re_matches

def rotate_l (sequence) :
    """Return a copy of sequence that is rotated left by one element

       >>> rotate_l ([1, 2, 3])
       [2, 3, 1]
       >>> rotate_l ([1])
       [1]
       >>> rotate_l ([])
       []
    """
    return sequence [1:] + sequence [:1]
# end def rotate_l

def rotate_r (sequence) :
    """Return a copy of sequence that is rotated right by one element

       >>> rotate_r ([1, 2, 3])
       [3, 1, 2]
       >>> rotate_r ([1])
       [1]
       >>> rotate_r ([])
       []
    """
    return sequence [-1:] + sequence [:-1]
# end def rotate_r

def rounded_down (value, granularity) :
    """Returns `value` rounded down to nearest multiple of `granularity`.

       >>> rounded_down (3, 5)
       0
       >>> rounded_down (8, 5)
       5
       >>> rounded_down (5, 5)
       5
       >>> rounded_down (-3, 5)
       -5
       >>> rounded_down (-8, 5)
       -10
    """
    return value - (value % granularity)
# end def rounded_down

def rounded_to (value, granularity) :
    """Returns `value` rounded to nearest multiple of `granularity`.

       >>> [rounded_to (v, 15) for v in [0, 1, 7, 8, 14, 22, 23]]
       [0, 0, 0, 15, 15, 15, 30]
       >>> [rounded_to (-v, 15) for v in [0, 1, 7, 8, 14, 22, 23]]
       [0, 0, 0, -15, -15, -15, -30]
    """
    rd = rounded_down (value, granularity)
    ru = rounded_up   (value, granularity)
    if abs (ru - value) < abs (value - rd) :
        return ru
    else :
        return rd
# end def rounded_to

def rounded_up (value, granularity) :
    """Returns `value` rounded up to nearest multiple of `granularity`.

       >>> rounded_up (3, 5)
       5
       >>> rounded_up (8, 5)
       10
       >>> rounded_up (-3, 5)
       0
       >>> rounded_up (-8, 5)
       -5
    """
    return value + ((granularity - value) % granularity)
# end def rounded_up

def second_arg (x, y, * args, ** kw) :
    """Returns the second argument unchanged"""
    return y
# end def second_arg

def sliced (iterable, length) :
    """Generate all slices of size `length` in `iterable`.

        >>> l = range (20)
        >>> for s in sliced (l, 3) :
        ...   print s
        ...
        (0, 1, 2)
        (3, 4, 5)
        (6, 7, 8)
        (9, 10, 11)
        (12, 13, 14)
        (15, 16, 17)
        (18, 19)
        >>> for s in sliced (l, 5) :
        ...   print s
        ...
        (0, 1, 2, 3, 4)
        (5, 6, 7, 8, 9)
        (10, 11, 12, 13, 14)
        (15, 16, 17, 18, 19)
        >>> for s in sliced (l, 8) :
        ...   print s
        ...
        (0, 1, 2, 3, 4, 5, 6, 7)
        (8, 9, 10, 11, 12, 13, 14, 15)
        (16, 17, 18, 19)
        >>> for s in sliced (l, 10) :
        ...   print s
        ...
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        (10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
    """
    it = iter (iterable)
    while True :
        next = tuple (itertools.islice (it, None, length))
        if next :
            yield next
        else :
            break
# end def sliced

### Legacy: allow `sorted` to be passed to `_Export`
sorted = sorted

def split_by_key (seq, key_cmp, min_result_size = 1) :
    """Returns a list of lists each containing the elements of `seq' with a
       single key as determined by `key_cmp'.

       The result is sorted by `key_cmp'.
    """
    result = [[]]
    source = sorted (seq, key_cmp)
    if source :
        for (a, b) in TFL.pairwise (source) :
            result [-1].append (a)
            if key_cmp (a, b) != 0 :
                result.append ([])
        result [-1].append (source [-1])
    if len (result) < min_result_size :
        result = result + ([[]] * (min_result_size - len (result)))
    return result
# end def split_by_key

def split_hst (string, sep) :
    """Returns a three element tuple (head, sep, tail) with
       `"".join (split_hst (string)) == string` split around the
       first occurrence of `sep`.

       Based on Raymond Hettinger's proposal for a new
       string-method `str.partition` (python-dev@python.org).

       In a later post to python-dev@python.org, Nick Coghlan
       explained the semantics nicely:

           head and not sep and not tail (the separator was not found)
           head and sep and not tail (the separator is at the end)
           head and sep and tail (the separator is somewhere in the middle)
           not head and sep and tail (the separator is at the start)
           not head and sep and not tail (the separator is the whole string)

       >>> split_hst ("a", ",")
       ('a', '', '')
       >>> split_hst ("a,b", ",")
       ('a', ',', 'b')
       >>> split_hst ("a,b,c", ",")
       ('a', ',', 'b,c')
       >>> split_hst (",a", ",")
       ('', ',', 'a')
       >>> split_hst (",a,b", ",")
       ('', ',', 'a,b')
       >>> split_hst ("a,", ",")
       ('a', ',', '')
       >>> split_hst ("a,b", "b")
       ('a,', 'b', '')
       >>> split_hst ("a,bb", "b")
       ('a,', 'b', 'b')
       >>> split_hst (",", ",")
       ('', ',', '')
    """
    parts = string.split (sep, 1)
    if len (parts) == 1 :
        return parts [0], "", ""
    else :
        return parts [0], sep, parts [1]
# end def split_hst

def rsplit_hst (string, sep) :
    """Returns a three element tuple (tail, sep, head) with
       `"".join (rsplit_hst (string)) == string` split around the
       last (i.e., rightmost) occurrence of `sep`.

       Based on Raymond Hettinger's proposal for a new
       string-method `str.rpartition` (python-dev@python.org).

       >>> rsplit_hst ("a", ",")
       ('', '', 'a')
       >>> rsplit_hst ("a,b", ",")
       ('a', ',', 'b')
       >>> rsplit_hst ("a,b,c", ",")
       ('a,b', ',', 'c')
       >>> rsplit_hst (",a", ",")
       ('', ',', 'a')
       >>> rsplit_hst (",a,b", ",")
       (',a', ',', 'b')
       >>> rsplit_hst ("a,b", "b")
       ('a,', 'b', '')
       >>> rsplit_hst ("a,bb", "b")
       ('a,b', 'b', '')
       >>> rsplit_hst (",", ",")
       ('', ',', '')
    """
    parts = string.rsplit (sep, 1)
    if len (parts) == 1 :
        return "", "", parts [0]
    else :
        return parts [0], sep, parts [1]
# end def rsplit_hst

def string_cross_sum (string) :
    return cross_sum (string, ord)
# end def string_cross_sum

def successor_of (element, iterable, pairwise = pairwise) :
    """Returns the successor of `element` in `iterable`"""
    for (l, r) in pairwise (iterable) :
        if l == element :
            return r
    raise IndexError
# end def successor_of

def tail_slices (l) :
    """Returns the list of all slices anchored at tail of `l'

       >>> tail_slices ("abcdef")
       ['abcdef', 'bcdef', 'cdef', 'def', 'ef', 'f']
    """
    return [l [i:] for i in range (len (l))]
# end def tail_slices

def third_arg (x, y, z, * args, ** kw) :
    """Returns the third argument unchanged"""
    return z
# end def third_arg

def tupelize (l) :
    """Converts every occurance of a list to a tuple. Afterwards `l` should
       be hashable.

       >>> tupelize ([1, 2, 3])
       (1, 2, 3)
       >>> tupelize ([])
       ()
       >>> tupelize ([1, 2, [3], [4, [5, 6]]])
       (1, 2, (3,), (4, (5, 6)))
    """
    if isinstance (l, (str, unicode)) :
        return l
    try:
        l = list (l)
        for i, e in enumerate (l) :
            l [i] = tupelize (e)
        return tuple (l)
    except TypeError :
        return l
# end def tupelize

def undotted_dict (d, sep = ".") :
    """Return a dict with un-dotted keys. Dotted keys in `d` are converted
       to nested dictionaries with un-dotted keys in the result.

       >>> def show (d) :
       ...     def gen (d) :
       ...         for k, v in sorted (d.iteritems ()) :
       ...             if isinstance (v, dict) :
       ...                 v = show (v)
       ...             yield "%r : %s" % (k, v)
       ...     return "{%s}" % (", ".join (gen (d)))
       ...
       >>> show (undotted_dict({"a" : 1, "ab.b" : 2}))
       "{'a' : 1, 'ab' : {'b' : 2}}"
       >>> show (undotted_dict({"a" : 1, "ab.b" : 2, "ab.c.d" : 42}))
       "{'a' : 1, 'ab' : {'b' : 2, 'c' : {'d' : 42}}}"
    """
    result = {}
    for k, v in sorted (d.iteritems ()) :
        n = k
        target = result
        if sep in k :
            os, _, n = rsplit_hst (k, sep)
            for o in os.split (sep) :
                target = target.setdefault (o, {})
                assert isinstance (target, dict), "Need a dict: %s, %s" % (o, k)
        target [n] = v
    return result
# end def undotted_dict

def dotted_dict (d, prefix = "", sep = ".") :
    """Return a flat dict where sub-dicts will be merged into the top level
       dict and the keys will be combined with `.`s

       >>> def show (d) :
       ...     for k, v in sorted (d.iteritems ()) :
       ...         print k, v
       >>> show (dotted_dict (dict (a = 1, b = dict (c = 2, d = dict (e = 3)))))
       a 1
       b.c 2
       b.d.e 3
    """
    result = {}
    if prefix :
        prefix = "%s%s" % (prefix, sep)
    for k, v in d.iteritems () :
        k = "%s%s" % (prefix, k)
        if isinstance (v, dict) :
            result.update (dotted_dict (v, k, sep))
        else :
            result [k] = v
    return result
# end def dotted_dict

def union (* lists) :
    """Compute the union of lists.

       >>> sorted (union (range (3), range (42, 45)))
       [0, 1, 2, 42, 43, 44]
    """
    result = set ()
    for l in lists :
        result.update (l)
    return result
# end def union

def uniq (seq) :
    """Returns a copy of `seq` where duplicates are eliminated while
       preserving the order of the remaining elements.

       >>> list (uniq ([]))
       []
       >>> list (uniq ([1]))
       [1]
       >>> list (uniq ([1, 2, 3]))
       [1, 2, 3]
       >>> list (uniq ([1, 1, 1]))
       [1]
       >>> list (uniq ([1, 2, 2, 3, 4, 4]))
       [1, 2, 3, 4]
       >>> list (uniq ([1, 2, 3, 2, 4, 1]))
       [1, 2, 3, 4]
    """
    seen = set ()
    for e in seq :
        if e not in seen :
            seen.add (e)
            yield e
# end def uniq

def uniq_p (seq, pred) :
    """Returns a copy of `seq` where duplicates with regard to `pred` are
       eliminated while preserving the order of the remaining elements.

       >>> range (1, 60, 5)
       [1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56]
       >>> list (uniq_p (range (1, 60, 5), lambda x : x%6))
       [1, 6, 11, 16, 21, 26]
    """
    seen = set ()
    for e in seq :
        p = pred (e)
        if p not in seen :
            seen.add (p)
            yield e
# end def uniq_p

def un_nested (l) :
    """Returns list `l' in un-nested form (i.e., if it is a one-element list
       whose first element is a list, returns l [0]).

       This is handy if you want to support the passing of a list to a `*
       args' argument without using `apply'.

       >>> un_nested (range (3))
       [0, 1, 2]
       >>> un_nested ([range (3)])
       [0, 1, 2]
       >>> un_nested ([range (3), range (2)])
       [[0, 1, 2], [0, 1]]
    """
    if l and len (l) == 1 and isinstance (l [0], (list, tuple)) :
        l = l [0]
    return l
# end def un_nested

def xored_string (source, salt = "�") :
    salt = ord (salt)
    return "".join (chr (ord (c) ^ salt) for c in source)
# end def xored_string

if __name__ != "__main__" :
    TFL._Export ("*", "sorted", "reversed")
### __END__ TFL.predicate
