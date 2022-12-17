Nested Markov Chain for Generating Test Data for Compression
============================================================

This project implements "Nested Markov Chain" in a Python script for 
generating data for testing lossless data compressors.

The Implementation
------------------

The `NestedMarkovChain` class implements the behaviors of a Markov chain.
When instantiating, it takes an argument that defines the states and their
associated transition probability, and creates and returns an iterable object
that generates data according to the so-defined Markov chain.

The `NMCFactory` class is a easy wrapper that generates a Markov chain states
definition for use in instantiating `NestedMarkovChain` objects.

Using the Script
----------------

When run directly, the script:

1. creates a master Markov chain of 5 states,

2. assign the first 3 states each a Markov chain for generating bytes and 
   reserve 2 for dynamically changing Markov chains

3. invokes the master Markov chain to transition between the byte-generating
   Markov chains. When reserved states are reached, a brand-new byte-generating
   Markov chain is created to generate data until it reaches exit point, at
   which time the master Markov chain will continue to transition between
   the byte-generating Markov chains.

4. exits when the master Markov chain reaches exit point.
