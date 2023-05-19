import pytest
from ase import build, db
from ase.io import write
import os

from ocpmodels.datasets import AseReadDataset, AseDBDataset

structures = [
    build.molecule("H2O", vacuum=4),
    build.bulk("Cu"),
    build.fcc111("Pt", size=[2, 2, 3], vacuum=8, periodic=True),
]


def test_ase_read_dataset():
    for i, structure in enumerate(structures):
        write(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), f"{i}.cif"
            ),
            structure,
        )

    dataset = AseReadDataset(
        config={
            "src": os.path.join(os.path.dirname(os.path.abspath(__file__))),
            "pattern": "*.cif",
        }
    )

    assert len(dataset) == len(structures)
    data = dataset[0]

    for i in range(len(structures)):
        os.remove(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), f"{i}.cif"
            )
        )


def test_ase_db_dataset():
    try:
        os.remove(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "asedb.db"
            )
        )
    except FileNotFoundError:
        pass

    database = db.connect(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "asedb.db")
    )
    for i, structure in enumerate(structures):
        database.write(structure)

    dataset = AseDBDataset(
        config={
            "src": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "asedb.db"
            ),
        }
    )

    assert len(dataset) == len(structures)
    data = dataset[0]

    os.remove(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "asedb.db")
    )


def test_ase_lmdb_dataset():
    try:
        os.remove(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "asedb.lmdb"
            )
        )
    except FileNotFoundError:
        pass

    database = db.connect(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "asedb.lmdb")
    )
    for i, structure in enumerate(structures):
        database.write(structure)

    dataset = AseDBDataset(
        config={
            "src": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "asedb.lmdb"
            ),
        }
    )

    assert len(dataset) == len(structures)
    data = dataset[0]

    os.remove(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "asedb.lmdb")
    )