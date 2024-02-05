if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    zero_passagers_count = data['passenger_count'].isin([0]).sum()
    zero_trip_distance_count = data['trip_distance'].isin([0]).sum()

    # question_four = data['VendorID'].unique()
    # print(f"Question Four: {question_four}")
    # Question Four: [ 2.  1. nan]

    print(f"Rows with passenger count = 0: {zero_passagers_count}")
    return data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]


@test
def test_no_zero_passenger_data(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with 0 passengers'

@test
def test_no_zero_trip_distance_data(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with 0 passengers'

# 139,370 rows
