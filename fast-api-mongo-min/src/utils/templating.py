# Yan Pan
# modify the delimiter for Jinja2 to support Vue.JS actions
from fastapi.templating import Jinja2Templates

TEMPLATES_ALT = Jinja2Templates(
    directory="templates",
    block_start_string='[%',
    block_end_string='%]',
    variable_start_string='[[',
    variable_end_string=']]',
    comment_start_string='{#',
    comment_end_string='#}',
)
