#!/usr/bin/env bash
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
MODELDIR=data/model/lstm_siam
SRCDIR=src/similarity/lstm_siam

echo "Prepare Train Data"
python "${SRCDIR}"/trans_format.py

echo "Start to train LSTM"
python "${SRCDIR}"/train.py \
    --is_char_based False \
    --word2vec_model "${MODELDIR}"/wordvector.tsv \
    --word2vec_format text \
    --embedding_dim 128 \
    --dropout_keep_prob 0.6 \
    --training_files "${MODELDIR}"/train_data.tsv