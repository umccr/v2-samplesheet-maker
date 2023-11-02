FROM python:3-slim

ARG V2_SAMPLESHEET_MAKER_VERSION_TAG
ARG INDEX_URL="https://pypi.org/simple/"
ARG EXTRA_INDEX_URL="https://pypi.org/simple/"

RUN \
  pip install pip \
    --no-cache-dir \
    --upgrade && \
  pip install "v2-samplesheet-maker==${V2_SAMPLESHEET_MAKER_VERSION_TAG}" \
    --index-url "${INDEX_URL}" \
    --extra-index-url "${EXTRA_INDEX_URL}" \
    --no-cache-dir

CMD v2-samplesheet-maker