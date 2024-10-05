#  == WORKER ==
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from worker.db_store import DBStore, DB
from worker.file_store import FileStore
from worker.person_web_repository import PersonWebRepository
from worker.person_local_repository import PersonLocalRepository


#
# WOKER 는 프로젝트에서 본격적인 일을 하는 객체로서,
# WORKING 프로토콜에 정의된 임무를 수행합니다.
# 구체적으로는, GEAR 와 UITL 을 이용하여 WORKING 요구사항을 충족합니다.
# 모든 에러 핸들링을 처리하며, 사용자에게 알릴 오류는 Fizzle 을 사용합니다.
# 현 프로젝트에 종속적입니다. 재활용할 수 없습니다.
#
