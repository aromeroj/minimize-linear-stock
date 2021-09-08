import copy
import sys
import getopt

CUT_LENGTH_INDEX = 0
NUMBER_OF_CUTS_INDEX = 1


def reduce_stock_used(stock_length, stocks_used, cut_length, remaining_stock_length, required_cuts, performed_cuts):
    if cut_length > 0:
        if cut_length <= remaining_stock_length and remaining_stock_length > 0:
            remaining_stock_length -= cut_length
            current_stock_cuts = performed_cuts[len(performed_cuts) - 1]
            current_stock_cuts.append(cut_length)
        else:
            stocks_used += 1
            remaining_stock_length = stock_length - cut_length
            first_cut = [cut_length]
            performed_cuts.append(first_cut)
        perform_cut(cut_length, required_cuts)
    if cuts_completed(required_cuts):
        return stocks_used, performed_cuts
    min_used_stock = float('inf')
    min_performed_cuts = None
    for required_cut in required_cuts:
        if required_cut[NUMBER_OF_CUTS_INDEX] > 0:
            stocks, cuts_made = reduce_stock_used(
                stock_length, stocks_used, required_cut[CUT_LENGTH_INDEX], remaining_stock_length,
                copy.deepcopy(required_cuts), copy.deepcopy(performed_cuts))
            if stocks < min_used_stock:
                min_used_stock = stocks
                min_performed_cuts = cuts_made
    return min_used_stock, min_performed_cuts


def cuts_completed(required_cuts):
    for required_cut in required_cuts:
        if required_cut[NUMBER_OF_CUTS_INDEX] > 0:
            return False
    return True


def perform_cut(cut_length, required_cuts):
    for required_cut in required_cuts:
        if required_cut[CUT_LENGTH_INDEX] == cut_length:
            required_cut[NUMBER_OF_CUTS_INDEX] = required_cut[NUMBER_OF_CUTS_INDEX] - 1
            return


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:c:", ["help", "stock_length", "cut_list"])
    except getopt.GetoptError as err:
        print(err)
        usage(__file__)
        sys.exit(2)

    stock_length = 0
    required_cuts = []

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage(__file__)
        elif opt in ("-s", "--stock_length"):
            stock_length = int(arg)
        elif opt in ("-c", "--cut_list"):
            cut_list = arg.replace(" ", "")
            required_cuts = cut_list.split(':')
            for i in range(len(required_cuts)):
                required_cuts[i] = [int(x) for x in required_cuts[i].split(',')]

    requirements_complete = True
    if stock_length == 0:
        print('stock_length is required')
        requirements_complete = False
    if not required_cuts:
        print('cut_list is required')
        requirements_complete = False

    if not requirements_complete:
        usage(__file__)
    else:
        stocks, cuts = reduce_stock_used(stock_length, 0, -1, 0, required_cuts, [])
        print('Number of stocks required: ' + str(stocks))
        for i in range(len(cuts)):
            print('Stock ' + str(i + 1) + ', cuts: ' + str(cuts[i])
                  + ', remaining: ' + str(stock_length - sum(cuts[i])))


def usage(filename):
    print(filename + ' -s <stock_length> -c <cut_list>')
    print('# Each cut from <cut_list> must by separated by colon, '
          'each cut contains the length and quantity separated by a comma')
    print('# Example: 4,2:8,5:2,3')


if __name__ == "__main__":
    main()
