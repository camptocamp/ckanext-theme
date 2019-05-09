import logging

from ckan import model
from ckan.controllers.organization import OrganizationController as CkanBaseOrganizationController
from ckan.common import c, request, _
import ckan.lib.helpers as h
from ckan.lib import base
from ckan.logic import NotAuthorized, ValidationError

log = logging.getLogger(__name__)

render = base.render
abort = base.abort

class OrganizationController(CkanBaseOrganizationController):
    """
    Extend the OrganizationController. OrganizationController share a large amount of code with group.

    Also all the code is implemented for groups and adapt for orgs.
    """

    def index(self):
        '''
        This is a copy of ckan.controller.groups.GroupController.

        Since the original method return bytes (from the render function) we can't call super() and treat the response
        This function doesn't use a lot of sub-function too so, as a workaround, we copied the original code, place the
         original code in pre_processing and render function in order to make it maintainable. Note that the "21" magic
         number is also a magic number in the GroupController impl.
        '''
        all_orgs = self._pre_processing()
        page = self._get_page()
        filtered_orgs = self._filter_orgs_with_empty_dataset(all_orgs)
        page_orgs = self._get_paginate_content(filtered_orgs, page)

        return self._render(filtered_orgs, page_orgs, page)

    def _get_page(self):
        return h.get_page_number(request.params) or 1

    def _filter_orgs_with_empty_dataset(self, orgs):
        filtered_orgs = list(filter(lambda x: x['package_count'] > 0, orgs))
        log.info('{} orgs fetched, {} orgs after filtering'.format(len(orgs), len(filtered_orgs)))
        return filtered_orgs


    def _get_paginate_content(self, results, page):
        items_per_page = 21
        offset = items_per_page * (page - 1)
        final_offset = offset if offset else 1
        r = results[offset:items_per_page+final_offset]
        return r

    def _pre_processing(self):
        group_type = self._guess_group_type()
        context = {'model': model, 'session': model.Session,
                   'user': c.user, 'for_view': True,
                   'with_private': False}

        q = c.q = request.params.get('q', '')
        sort_by = c.sort_by_selected = request.params.get('sort')
        try:
            self._check_access('site_read', context)
            self._check_access('group_list', context)
        except NotAuthorized:
            abort(403, _('Not authorized to see this page'))

        # pass user info to context as needed to view private datasets of
        # orgs correctly
        if c.userobj:
            context['user_id'] = c.userobj.id
            context['user_is_admin'] = c.userobj.sysadmin

        try:
            data_dict_global_results = {
                'all_fields': True,
                'q': q,
                'sort': sort_by,
                'type': group_type or 'group',
                'include_extras': True
            }
            global_results = self._action('group_list')(
                context, data_dict_global_results)
        except ValidationError as e:
            if e.error_dict and e.error_dict.get('message'):
                msg = e.error_dict['message']
            else:
                msg = str(e)
            h.flash_error(msg)
            c.page = h.Page([], 0)
            return render(self._index_template(group_type),
                          extra_vars={'group_type': group_type})

        # we removed from the original impl the second db request to get a filtered view of orgs.

        return global_results


    def _render(self, global_results, page_results, page):
        c.page = h.Page(
            collection=global_results,
            page=page,
            url=h.pager_url,
            items_per_page=21,  # since this is hardcoded in the ckan base class...
        )

        c.page.items = page_results
        return render(self._index_template('organization'),
                      extra_vars={'group_type': 'organization'})