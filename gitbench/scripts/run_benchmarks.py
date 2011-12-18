def run_benchmarks(benchmarks, outfile):
    results = []

    for bmk in benchmarks:
        res = bmk.run()
        results.append(res)

if __name__ == '__main__':
    import optparse
    parser = optparse.OptionParser(
        usage="%prog [options]",
        description=("Test the performance of pickling."))
    parser.add_option("--input", action="store",
                      help="Pickle file containing list of benchmark objects")
    parser.add_option("--output", action="store",
                      help="File path to store pickled results")
    options, args = parser.parse_args()

    print options.input
    print options.output

