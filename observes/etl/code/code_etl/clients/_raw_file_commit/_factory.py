from code_etl.clients._raw_objs import (
    RawFileCommitRelation,
)
from code_etl.objs import (
    CommitStamp,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    PureIter,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)


@dataclass(frozen=True)
class FileRelationFactory:
    @staticmethod
    def extract_relations(
        stamp: CommitStamp,
    ) -> PureIter[RawFileCommitRelation]:
        def _build(file: str) -> RawFileCommitRelation:
            return RawFileCommitRelation(
                stamp.commit.commit_id.repo.namespace,
                stamp.commit.commit_id.repo.repository,
                stamp.commit.commit_id.hash.hash,
                file,
            )

        empty: PureIter[RawFileCommitRelation] = from_flist(tuple())
        return stamp.commit.data.files.map(
            lambda f: from_flist(tuple(f)).map(_build)
        ).value_or(empty)
