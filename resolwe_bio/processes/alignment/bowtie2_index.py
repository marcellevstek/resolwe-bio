"""Create genome index for Bowtie2 aligner."""
import shutil
from pathlib import Path

from plumbum import TEE

from resolwe.process import Cmd, DataField, DirField, FileField, Process, StringField


class Bowtie2Index(Process):
    """Create Bowtie2 genome index."""

    slug = "bowtie2-index"
    process_type = "data:index:bowtie2"
    name = "Bowtie2 genome index"
    requirements = {
        "expression-engine": "jinja",
        "executor": {
            "docker": {"image": "public.ecr.aws/genialis/resolwebio/rnaseq:6.0.0"},
        },
        "resources": {
            "cores": 10,
            "memory": 16384,
        },
    }
    category = "Genome index"
    data_name = '{{ ref_seq.fasta.file|basename|default("?") }}'
    version = "1.2.0"

    class Input:
        """Input fields for Bowtie2Index."""

        ref_seq = DataField(
            "seq:nucleotide", label="Reference sequence (nucleotide FASTA)"
        )

    class Output:
        """Output fields to process Bowtie2Index."""

        index = DirField(label="Bowtie2 index")
        fastagz = FileField(label="FASTA file (compressed)")
        fasta = FileField(label="FASTA file")
        fai = FileField(label="FASTA file index")
        species = StringField(label="Species")
        build = StringField(label="Build")

    def run(self, inputs, outputs):
        """Run analysis."""
        basename = Path(inputs.ref_seq.output.fasta.path).name
        assert basename.endswith(".fasta")
        name = basename[:-6]

        index_dir = Path("bowtie2_index")
        index_dir.mkdir()

        shutil.copy(Path(inputs.ref_seq.output.fasta.path), Path.cwd())
        shutil.copy(Path(inputs.ref_seq.output.fastagz.path), Path.cwd())
        shutil.copy(Path(inputs.ref_seq.output.fai.path), Path.cwd())

        args = [
            inputs.ref_seq.output.fasta.path,
            index_dir / f"{name}_index",
            "--threads",
            self.requirements.resources.cores,
        ]

        return_code, _, _ = Cmd["bowtie2-build"][args] & TEE(retcode=None)
        if return_code:
            self.error("Error occurred while preparing the Bowtie2 index.")

        outputs.index = index_dir.name
        outputs.fasta = f"{name}.fasta"
        outputs.fastagz = f"{name}.fasta.gz"
        outputs.fai = f"{name}.fasta.fai"
        outputs.species = inputs.ref_seq.output.species
        outputs.build = inputs.ref_seq.output.build
