#!/usr/bin/env python3

import itertools
import statistics

import nltk_tgrep


# Average number of CONSTITUENTs per sentence (NP, VP, PP, SBAR)

# Average length of CONSTITUENT (NP, VP, PP)

# Average number of constituents per sentence

# NUR = FRAG?

# Lu 2010


def _average_statistic_with_lengths(statistic, trees):
    """Calculate the statistic for every sentence and return mean and
    standard deviation."""
    results = [statistic(t) for t in trees]
    counts, lengths = zip(*results)
    lengths = list(itertools.chain.from_iterable(lengths))
    return statistics.mean(counts), statistics.stdev(counts), statistics.mean(lengths), statistics.stdev(lengths)


def _average_statistic_wo_lengths(statistic, trees):
    """Calculate the statistic for every sentence and return mean and
    standard deviation."""
    results = [statistic(t) for t in trees]
    return statistics.mean(results), statistics.stdev(results)


def average_t_units(trees):
    return _average_statistic_with_lengths(t_units, trees)


def t_units(tree):
    """A t-unit is “one main clause plus any subordinate clause or
    nonclausal structure that is attached to or embedded in it” (Hunt
    1970: 4).

    We operationalize it as an S node that is immediately dominated
    either by TOP or by a CS node that is immediately dominated by
    TOP. S = sentence, CS = coordinated sentence.

    """
    return _single_constituent(tree, "S > (CS > TOP) | > TOP")


def average_clauses(trees):
    return _average_statistic_with_lengths(clauses, trees)


def clauses(tree):
    """A clause is defined as a structure with a subject and a finite verb
    (Hunt 1965, Polio 1997).

    We operationalize it as an S node, since that is defined as “a
    finite verb + its dependents”.
    (http://www.coli.uni-saarland.de/projects/sfb378/negra-corpus/knoten.html#S).

    """
    return _single_constituent(tree, "S")


def average_nps(trees):
    return _average_statistic_with_lengths(nps, trees)


def nps(tree):
    """Number and lengths of NPs."""
    return _single_constituent(tree, "NP")


def average_vps(trees):
    return _average_statistic_with_lengths(vps, trees)


def vps(tree):
    """Number and lengths of VPs."""
    return _single_constituent(tree, "VP")


def average_pps(trees):
    return _average_statistic_with_lengths(pps, trees)


def pps(tree):
    """Number and lengths of PPs."""
    return _single_constituent(tree, "PP")


def average_constituents(trees):
    return _average_statistic_wo_lengths(constituents, trees)


def constituents(tree):
    """Number of constituents."""
    return len(list(tree.subtrees()))


def average_constituents_wo_leaves(trees):
    return _average_statistic_wo_lengths(constituents_wo_leaves, trees)


def constituents_wo_leaves(tree):
    """Number of constituents (not counting leaves)."""
    return len(list(tree.subtrees())) - len(tree.leaves())


def _single_constituent(tree, constituent):
    """Number and lenghts of constituent"""
    result = nltk_tgrep.tgrep_nodes(tree, constituent)
    lengths = [len(r.leaves()) for r in result]
    return len(result), lengths
