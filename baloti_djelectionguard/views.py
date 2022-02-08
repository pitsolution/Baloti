import json
from django.shortcuts import render
from djelectionguard.models import Contest, Candidate, ParentContest
from django.db.models import ObjectDoesNotExist, Q
from django.http import *
from django.views.generic import TemplateView
from djlang.utils import gettext as _
from electeez_common.components import *
import hashlib
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from electeez_auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def getParentDetails(parent):
        """
        Args:
            @param id - parent

        Returns:
            @return array
        """
        data = {
            'name': parent.name,
            'id': parent.uid,
            'date': parent.start.date(),
            'month': parent.start.strftime('%B'),
            'year': parent.start.strftime('%Y'),
            'status': parent.status,
            }
        return data

class BalotiIndexView(TemplateView):
    """
    Index view.
    """

    def get(self, request):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns contest_list.html html file
        """
        contests = []
        open_contests = ParentContest.objects.filter(status="open").order_by('-actual_start')
        contests.append(getParentDetails(open_contests[0])) if open_contests else None
        closed_contests = ParentContest.objects.filter(status="closed").order_by('-actual_end')
        contests.append(getParentDetails(closed_contests[0])) if closed_contests else None
        return render(request, 'index.html',{"contests": contests})

class BalotiNewsView(TemplateView):
    """
    News View
    """
    template_name = "news.html"

class BalotiDisclaimerView(TemplateView):
    """
    Disclaimer View
    """
    template_name = "disclaimer.html"

class BalotiImprintView(TemplateView):
    """
    Imprint View
    """
    template_name = "imprint.html"

    def get(self, request):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns imprint.html html file
        """
        return render(request, 'imprint.html')

class BalotiDataPrivacyView(TemplateView):
    """
    Data Privacy View
    """
    template_name = "data_privacy.html"

    def get(self, request):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns data_privacy.html html file
        """
        return render(request, 'data_privacy.html')



class BalotiAboutUsView(TemplateView):
    """
    AboutUs View
    """
    template_name = "about-us.html"

class BalotiInfoView(TemplateView):
    """
    Info View
    """

    def get(self, request):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns landing-en.html html file
        """
        return render(request, 'landing-en.html')

    def post(self, request):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns landing-en.html html file
        """
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email_from = settings.DEFAULT_FROM_EMAIL
        email_to = 'baloti@pitsolutions.ch'
        if firstname and lastname and email and subject and message:
            merge_data = {
                        'firstname': firstname,
                        'lastname': lastname,
                        'email': email,
                        'message': message
                        }
            html_body = render_to_string("contactinfo_mail.html", merge_data)

            message = EmailMultiAlternatives(
               subject=subject,
               body="mail testing",
               from_email=email_from,
               to=[email_to],
            )
            message.attach_alternative(html_body, "text/html")
            message.send()
            messages.success(self.request, _('dcfxv sent by email'))
            responseData = {}
            return HttpResponse(json.dumps(responseData), content_type="application/json")
        else:
            return HttpResponseBadRequest()


class BalotiContestListView(TemplateView):
    """
    Contest List View
    """

    def get(self, request):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns contest_list.html html file
        """
        open_list = []
        closed_list = []
        open_contests = ParentContest.objects.filter(status="open").order_by('-actual_start')
        for open_contest in open_contests:
            open_list.append(getParentDetails(open_contest))
        closed_contests = ParentContest.objects.filter(status="closed").order_by('-actual_end')
        for closed_contest in closed_contests:
            closed_list.append(getParentDetails(closed_contest))
        return render(request, 'contest_list.html',{"open_contests": open_list, "closed_contests": closed_list})

class BalotiContestListSortView(TemplateView):
    """
    Contest List View
    """

    def get(self, request, sort):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns contest_list.html html file
        """
        open_list = []
        closed_list = []
        if sort == 'asc':
            open_contests = ParentContest.objects.filter(status="open").order_by('actual_start')
            closed_contests = ParentContest.objects.filter(status="closed").order_by('actual_end')
        else:
            open_contests = ParentContest.objects.filter(status="open").order_by('-actual_start')
            closed_contests = ParentContest.objects.filter(status="closed").order_by('-actual_end')
        for open_contest in open_contests:
            open_list.append(getParentDetails(open_contest))
        for closed_contest in closed_contests:
            closed_list.append(getParentDetails(closed_contest))
        return render(request, 'contest_list.html',{"open_contests": open_list, "closed_contests": closed_list})


class BalotiContestDetailView(TemplateView):
    """
    Contest Detail View
    """
    
    def get(self, request, id):
        """
        Args:
            request (Request): Http request object
            id: Contest UID

        Returns:
            html : returns contest_details.html html file
        """
        contest = ParentContest.objects.filter(uid=id)
        child_contests = Contest.objects.filter(
                parent=contest.first()
                ).distinct('id')
        date_string = contest.first().end.strftime("%m/%d/")
        return render(request, 'contest_details.html',{"contest": contest, "date": str(date_string), "child_contests": child_contests})


class BalotiContestResultView(TemplateView):
    """
    Contest Result View
    """

    def get(self, request, id):
        """
        Args:
            request (Request): Http request object
            id: Contest UID

        Returns:
            html : returns contest_results.html html file
        """
        contest = Contest.objects.filter(pk=id).first()
        return render(request, 'contest_results.html',{"contest": contest})


class BalotiContestChoicesView(TemplateView):
    """
    Contest Choices View
    """
    
    def get(self, request, id):
        """
        Args:
            request (Request): Http request object
            id: Candidate UID

        Returns:
            html : returns contest_vote_choices.html html file
        """
        contest = Contest.objects.get(pk=id)
        candidates = Candidate.objects.filter(contest=id)
        # return render(request, 'contest_vote_choices.html',{"candidates":candidates})
        if request.user.is_anonymous:
            return render(request, 'choice-no-login.html',{"contest": contest, "candidates":candidates})
        else:
            choice = request.GET.get('choice')
            return render(request, 'choice.html',{"contest": contest, "candidates":candidates})

    def post(self, request):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns login.html html file
        """
        contest = request.POST.get('contest')
        choice = request.POST.get('choice')
        if request.user.is_anonymous:
            return render(request, 'login.html',{'name':request.user, 'title':'Login', 'choice': choice})
        else:
            return VoteView().casteVote(request, choice)


class VoteView(TemplateView):
    """
    Vote Caste View
    """

    def get(self, request, id):
        """
        Args:
            request (Request): Http request object
            id: Candidate UID

        Returns:
            html : returns contest_details.html html file
        """
        return VoteView().casteVote(request, id)

def casteVote(self, request, id):
    """
    Args:
        request (Request): Http request object
        id: Candidate UID

    Returns:
        html : returns contest_details.html html file
    """
    user = request.user
    if not request.user.is_anonymous:
        candidate = Candidate.objects.filter(id=id)
        contest = Contest.objects.get(id=candidate.first().contest.id)
        candidates = Candidate.objects.filter(contest=contest)
        voter = contest.voter_set.filter(user=user)
        if voter and voter.first().casted:
            voter = voter.first()
            return render(request, 'vote_success.html',{"contest": contest, "candidates":candidates, "choice": candidate.first()})
            # return render(request, 'already_voted.html',{'user':user, 'title':'Already voted.'})
        else:
            ballot = contest.get_ballot(*[
                    selection.pk
                    for selection in candidate
                ])
            encrypted_ballot = contest.encrypter.encrypt(ballot)
            contest.ballot_box.cast(encrypted_ballot)

            submitted_ballot = contest.ballot_box._store.get(
                encrypted_ballot.object_id
            )
            ballot_sha1 = hashlib.sha1(
                submitted_ballot.to_json().encode('utf8'),
            ).hexdigest()

            contest.voter_set.update_or_create(
                user=user,
                defaults=dict(
                    casted=True,
                    ballot_id=encrypted_ballot.object_id,
                    ballot_sha1=ballot_sha1
                ),
            )
            contest.save()
            messages.success(
                    request,
                    _('You casted your ballot for %(obj)s', obj=contest)
                )
            return render(request, 'vote_success.html',{"contest": contest, "candidates":candidates, "choice": candidate.first()})
    else:
        return HttpResponseBadRequest()


class BalotiAnonymousVoteView(TemplateView):
    """
    Contest Anonymous Vote
    """

    def post(self, request):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns login.html html file
        """
        choice = request.POST.get('choice')
        return casteVote(self, request, choice)

class VoteSuccessView(TemplateView):
    """
    Contest Choices View
    """
    
    def get(self, request, id):
        """
        Args:
            request (Request): Http request object
            id: Candidate UID

        Returns:
            html : returns vote_success.html html file
        """
        return casteVote(self, request, id)
       
