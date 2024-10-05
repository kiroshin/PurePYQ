#  == SHOW ==
#  Created by Kiro Shin <mulgom@gmail.com> on 2024.

from show.item_data_user_role import ItemDataUserRole
from show.plain_list_model import PlainListModel, PlainListItem
from show.plain_list_view import PlainListView
from show.plain_searchbar import PlainSearchBar
from show.plain_table_model import PlainTableModel, PlainTableItem
from show.plain_table_view import PlainTableView
from show.profile_img_label import ProfileImgLabel
from show.text_item_delegate import TextItemDelegate
from show.toggle import Toggle


#
# SHOW 는 프로젝트에 독립적입니다. 따라서 상태를 가질 수 없습니다.
# SCREEN 에서 제공하는 상태에 따라 UI를 구성하며 갱신합니다.
# UTIL 을 참조하며 프로젝트 내부의 어떤 타입도 참조해서는 안 됩니다.
# 일부 컴포넌트는 GEAR 를 참조할 수 있는데, 이럴 경우 GEAR 는 싱글톤이나 순수함수로 동작해야 하며
# 특정 GEAR 유닛을 사용하는 것을 외부에서 모르게 해야 합니다.
#
