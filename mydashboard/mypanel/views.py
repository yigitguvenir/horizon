# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from horizon import tabs
from horizon import exceptions
from horizon import forms

from horizon.utils import memoized

from openstack_dashboard import api

from openstack_dashboard.dashboards.mydashboard.mypanel \
    import forms as project_forms

import subprocess
from django.http import HttpResponseRedirect
from horizon import tabs
from openstack_dashboard.dashboards.mydashboard.mypanel \
    import tabs as mydashboard_tabs


class IndexView(tabs.TabbedTableView):
    tab_group_class = mydashboard_tabs.MypanelTabs
    # A very simple class-based view...
    template_name = 'mydashboard/mypanel/index.html'

    def get_data(self, request, context, *args, **kwargs):
        # Add data to the context here...
        return 

    def post(self, request):
         target_ip = request.POST.get('target_id')
         server_type=request.POST.getlist("fav_language")
         subprocess.run(['./test1.sh','argument'], shell=True)
        #aaaa=request.post["asdasd"]
        #exit_code = subprocess.call('./test.sh')
        #bashCommand = "mkdir hellloo"
        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #output, error = process.communicate()
         return HttpResponseRedirect('/mydashboard')

class CreateSnapshotView(forms.ModalFormView):
    form_class = project_forms.CreateSnapshot
    template_name = 'mydashboard/mypanel/create_snapshot.html'
    success_url = reverse_lazy("horizon:project:images:index")
    modal_id = "create_snapshot_modal"
    modal_header = _("Create Snapshot")
    submit_label = _("Create Snapshot")
    submit_url = "horizon:mydashboard:mypanel:create_snapshot"

    @memoized.memoized_method
    def get_object(self):
        try:
            return api.nova.server_get(self.request,
                                       self.kwargs["instance_id"])
        except Exception:
            exceptions.handle(self.request,
                              _("Unable to retrieve instance."))

    def get_initial(self):
        return {"instance_id": self.kwargs["instance_id"]}

    def get_context_data(self, **kwargs):
        context = super(CreateSnapshotView, self).get_context_data(**kwargs)
        instance_id = self.kwargs['instance_id']
        context['instance_id'] = instance_id
        context['instance'] = self.get_object()
        context['submit_url'] = reverse(self.submit_url, args=[instance_id])
        return context
