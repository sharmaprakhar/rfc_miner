from artifact_extraction.data_utils import *
from artifact_extraction.models import *
from artifact_extraction.trainer import *

def run_nway(rfc_dir, annotated_rfcs, leave_out_rfc, window):
    # data array from text samples
    train_samples, train_labels = make(annotated_rfcs)
    test_samples, test_labels = make(leave_out_rfc)
    print('\ntotal train samples:',len(train_samples))
    print('total test samples:',len(test_samples))
    length_max = get_max_line(rfc_dir)
    allowed = get_char_vocab(rfc_dir, mode='minimal')
    print('len allowed:',len(allowed))
    num_feat = len(allowed)+1
    char_to_idx, idx_to_char = make_maps(allowed)
    train_samples = handle_newlines(train_samples, length_max)
    test_samples = handle_newlines(test_samples, length_max)
    
    # make data arrays
    X_train = create_samples_subset(train_samples, char_to_idx, length_max, allowed)
    y_train = np.array(train_labels)
    X_test = create_samples_subset(test_samples, char_to_idx, length_max, allowed)
    y_test = np.array(test_labels)
    
    # one hot encoding
    big_mat_train = make_one_hot_window(allowed, X_train)
    big_mat_test = make_one_hot_window(allowed, X_test)
    
    # data arr stats
    print('\ntrain data and labels shape:', big_mat_train.shape, y_train.shape)
    print('test data and labels shape:', big_mat_test.shape, y_test.shape)
    
    # flatten data matrices
    sh_train = big_mat_train.shape
    big_mat_train = big_mat_train.reshape(sh_train[0], -1)
    sh_test = big_mat_test.shape
    big_mat_test = big_mat_test.reshape(sh_test[0], -1)
    
    # stats
    print('\ntrain data:{} labels: {}'.format(big_mat_train.shape, y_train.shape))
    print('test data:{} labels: {}'.format(big_mat_test.shape, y_test.shape))
    
    # print class label stats
    how_many(y_train)
    how_many(y_test)

    # MODELING
    m = Trainer()
    m.split_and_create_loaders(big_mat_train, y_train)
    m.train_nway()