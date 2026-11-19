import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """

    # length of evidence lists and labels list should be equal to numbers of row in csv spreadsheet
    # this excluding the header

    evidences = []
    labels = []

    # lists ordered according to order users appear

    with open(filename, newline='') as file:
        mainfile = csv.reader(file)

        next(mainfile)

        # column that needs to be floating point
        float_pt = [1, 3, 5, 6, 7, 8, 9]

        # column that need to be int
        int_pt = [0, 2, 4, 10, 11, 12, 13, 14, 15, 16]

        # convert from month to index
        months = {
            'Jan': 0,
            'Feb': 1,
            'Mar': 2,
            'Apr': 3,
            'May': 4,
            'June': 5,
            'Jul': 6,
            'Aug': 7,
            'Sep': 8,
            'Oct': 9,
            'Nov': 10,
            'Dec': 11
        }

        # get each value for each category
        for values in mainfile:
            # get the label, which is the last value
            if values[-1] == 'TRUE':
                label = 1
            else:
                label = 0
            labels.append(label)

            # remove the label, so there's only evidence
            del values[-1]

            # get evidence
            # 17 values
            # change the data type of each columns
            # do float first and then int to make sure dont turn float string in int

            for i in range(len(values)):
                if i in float_pt:
                    values[i] = float(values[i])

                if i in int_pt:
                    # set condition for integers
                    if i == 10:
                        month = values[i]
                        values[i] = months[month]

                    elif i == 15:
                        if values[i] == 'Returning_Visitor':
                            values[i] = 1
                        else:
                            values[i] = 0

                    elif i == 16:
                        if values[i] == 'TRUE':
                            values[i] = 1
                        else:
                            values[i] = 0

                    else:
                        values[i] = int(values[i])

            # add each row
            evidences.append(values)

    return (evidences, labels)


    raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
