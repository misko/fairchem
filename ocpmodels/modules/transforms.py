import torch
from torch_geometric.data import Data

from ocpmodels.common.utils import cg_decomp_mat, irreps_sum
from ocpmodels.modules.normalizer import normalizer_transform as normalizer

_ = normalizer  # to avoid unused import error


class DataTransforms:
    def __init__(self, transform_config) -> None:
        self.transform_config = transform_config

    def __call__(self, data_object):
        if not self.transform_config:
            return data_object

        for transform in self.transform_config:
            for transform_fn in transform:
                data_object = eval(transform_fn)(
                    data_object, transform[transform_fn]
                )

        return data_object


def decompose_tensor(data_object, config) -> Data:
    tensor_key = config["tensor"]
    rank = config["rank"]

    if rank != 2:
        raise NotImplementedError

    tensor_decomposition = torch.einsum(
        "ab, cb->ca",
        cg_decomp_mat(rank),
        data_object[tensor_key].reshape(1, irreps_sum(rank)),
    )

    for decomposition_key in config["decomposition"]:
        irrep_dim = config["decomposition"][decomposition_key]["irrep_dim"]
        data_object[decomposition_key] = tensor_decomposition[
            :,
            max(0, irreps_sum(irrep_dim - 1)) : irreps_sum(irrep_dim),
        ]

    return data_object


def flatten(data_object, config) -> Data:
    tensor_key = config["tensor"]

    data_object[tensor_key] = data_object[tensor_key].reshape(1, -1)

    return data_object
