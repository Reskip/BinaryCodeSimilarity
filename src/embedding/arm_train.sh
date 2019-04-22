#!/usr/bin/env bash
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
MODELDIR=data/vector

mkdir -p "${MODELDIR}"

echo "Start to train"
src/embedding/StarSpace/starspace train \
  -trainFile "${MODELDIR}"/arm_train.tsv \
  -model "${MODELDIR}"/arm_embedding \
  -trainMode 5 \
  -initRandSd 0.01 \
  -adagrad true \
  -ngrams 1 \
  -lr 0.05 \
  -margin 0.05 \
  -epoch 20 \
  -thread 40 \
  -dim 128 \
  -negSearchLimit 100 \
  -dropoutRHS 0.8 \
  -similarity "cosine" \
  -minCount 5 \
  -normalizeText true \
  -verbose true