import json
import requests
from django.shortcuts import render
from djelectionguard.models import Contest, Candidate, ParentContest
from .models import ParentContesti18n, Contesti18n
from django.http import *
from django.views.generic import TemplateView
from djlang.utils import gettext as _
from electeez_common.components import *
import hashlib
from django.utils.translation import get_language
from electeez_auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from deep_translator import GoogleTranslator
from djlang.models import Language
from django.http import JsonResponse


def getParentDetails(parent):
        """
        Args:
            @param id - parent

        Returns:
            @return array
        """
        data = {
            'name': parent.name,
            'id': parent.parent_contest_id.uid,
            'iso':parent.language.iso,
            'date': parent.parent_contest_id.start.date(),
            'end_date': parent.parent_contest_id.end.date(),
            'month': parent.parent_contest_id.start.strftime('%B'),
            'year': parent.parent_contest_id.start.strftime('%Y'),
            'status': parent.parent_contest_id.status,
            }
        return data

class BalotiIndexView(TemplateView):
    """
    Index view.
    """

    def get(self, request, process=None):
        """
        Args:
            request (Request): Http request object

        Returns:
            html : returns index.html html file
        """
        contests = []
        current_language = get_language()
        open_contests = ParentContesti18n.objects.filter(parent_contest_id__status="open", language__iso=current_language).order_by('-parent_contest_id__start')
        contests.append(getParentDetails(open_contests[0])) if open_contests else None
        closed_contests = ParentContesti18n.objects.filter(parent_contest_id__status="closed", language__iso=current_language).order_by('-parent_contest_id__end')
        contests.append(getParentDetails(closed_contests[0])) if closed_contests else None
        if process == 'changepassword':
            return render(request, 'index.html',{"contests": contests, "changepassword":True})
        elif process == 'logout':
            return render(request, 'index.html',{"contests": contests, "logout":True})
        elif process == 'login':
            return render(request, 'index.html',{"contests": contests, "login":True})
        elif process == 'registration':
            return render(request, 'index.html',{"contests": contests, "registration":True})
        elif process == None:
            return render(request, 'index.html',{"contests": contests})
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
            JsonResponse: response with status message
        """
        captcha_token = request.POST.get('recaptcha_token', '')
        if not captcha_token:
            return JsonResponse({'error': 'reCAPTCHA token is missing.'}, status=400)
        try:
            recaptcha_response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data={
                    'secret': '6Ldk2Y8qAAAAAOmZYK6JgsWJVMgQkOaAGWc35Lju',
                    'response': captcha_token
                }
            )
            recaptcha_result = recaptcha_response.json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': f"Error during reCAPTCHA validation: {str(e)}"}, status=400)
        if not recaptcha_result.get('success') or recaptcha_result.get('score') < 0.5:
            return JsonResponse({'error': 'reCAPTCHA verification failed or score is too low.'}, status=400)
        if not all([request.POST.get('firstname'), request.POST.get('lastname'), request.POST.get('email'), request.POST.get('subject'), request.POST.get('message')]):
            return JsonResponse({'error': 'All fields are required.'}, status=400)
        merge_data = {
            'firstname': request.POST.get('firstname'),
            'lastname': request.POST.get('lastname'),
            'email': request.POST.get('email'),
            'message': request.POST.get('message'),
        }
        html_body = render_to_string("contactinfo_mail.html", merge_data)
        try:
            email_message = EmailMultiAlternatives(
                subject=request.POST.get('subject'),
                body="This is a contact message from your website.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.CONTACT_EMAIL_TO],
            )
            email_message.attach_alternative(html_body, "text/html")
            email_message.send()
        except Exception as e:
            return JsonResponse({'error': f"Error sending email: {str(e)}"}, status=400)
        return JsonResponse({
        'message': 'Your message has been sent successfully!',
        'recaptcha_result': recaptcha_result
    })


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
        current_language = get_language()
        open_contests = ParentContesti18n.objects.filter(parent_contest_id__status="open",language__iso=current_language).order_by('-parent_contest_id__start')
        for open_contest in open_contests:
            open_list.append(getParentDetails(open_contest))
        closed_contests = ParentContesti18n.objects.filter(parent_contest_id__status="closed",language__iso=current_language).order_by('-parent_contest_id__end')
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
        current_language = get_language()
        if sort == 'asc':
            open_contests = ParentContesti18n.objects.filter(parent_contest_id__status="open",language__iso=current_language).order_by('parent_contest_id__actual_start')
            closed_contests = ParentContesti18n.objects.filter(parent_contest_id__status="closed",language__iso=current_language).order_by('parent_contest_id__actual_end')
        else:
            open_contests = ParentContesti18n.objects.filter(parent_contest_id__status="open", language__iso=current_language).order_by('-parent_contest_id__actual_start')
            closed_contests = ParentContesti18n.objects.filter(parent_contest_id__status="closed", language__iso=current_language).order_by('-parent_contest_id__actual_end')
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
        current_language = get_language()
        contest = ParentContesti18n.objects.filter(parent_contest_id__uid=id, language__iso=current_language)
        child_contests = Contesti18n.objects.filter(
                parent=contest.first().parent_contest_id,
                language__iso=current_language
                ).distinct('id')
        date_string = contest.first().parent_contest_id.end.strftime("%m/%d/")
        return render(request, 'contest_details.html',{"contest": contest.first(), "date": str(date_string), "child_contests": child_contests})


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
        current_language = get_language()
        contest = Contesti18n.objects.filter(contest_id=id, language__iso=current_language).first()
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
        data = []
        current_language = get_language()
        language = Language.objects.filter(iso=current_language).first()
        contest = Contesti18n.objects.filter(contest_id=id, language__iso=current_language)
        if contest:
            contest = contest.first()
            candidates = Candidate.objects.filter(contest=contest.contest_id.id).order_by('-name')
            for candidate in candidates:
                data.append({
                    'name': GoogleTranslator('auto', language.dynamic_iso).translate(candidate.name),
                    'id': candidate.id
                    })
        # return render(request, 'contest_vote_choices.html',{"candidates":candidates})
        if request.user.is_anonymous:
            return render(request, 'choice-no-login.html',{"contest": contest, "candidates":data})
        else:
            choice = request.GET.get('choice')
            return render(request, 'choice.html',{"contest": contest, "candidates":data})

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
            return HttpResponse({'voted':True}, status=200)
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
        user = request.user
        if not request.user.is_anonymous:
            candidate = Candidate.objects.filter(id=id)
            contest = Contest.objects.get(id=candidate.first().contest.id)
            candidates = Candidate.objects.filter(contest=contest)
            voter = contest.voter_set.filter(user=user)
            if voter and voter.first().casted:
                return render(request, 'already_voted.html',{"contest": contest, "candidates":candidates, "choice": candidate.first()})
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
                return render(request, 'vote_success.html',{"contest": contest, "candidates":candidates, "choice": candidate.first()})
        else:
            return HttpResponseBadRequest()
