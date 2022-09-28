import pytz
from django.utils import timezone
from account.models import Teacher, Student, User
from qcm.models import Parcours, Studentanswer, Exercise, Demand
from school.models import School
from association.models import Accounting , Rate , Abonnement
from sendmail.models import Email, Message
from socle.models import Level
from school.models import School
from group.models import Group
from tool.models import Tool
from datetime import datetime 

##############################################################################################################################################
##############################################################################################################################################
###              L'établissement est-t-il membre sacado 
##############################################################################################################################################
##############################################################################################################################################


def is_sacado_asso(this_user, today):
    is_sacado = False
    is_active = False

    try :
        abonnement = this_user.school.abonnement.last()
        if today < abonnement.date_stop and abonnement.is_active :
            is_sacado = True
            is_active = True
    except :
        pass
    return is_sacado, is_active


##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################


def menu(request):

    if request.user.is_authenticated:

        is_gar_check = request.session.get("is_gar_check",None)

        try : # Vérifie qu'un user ne crée pas un compte annexe pour scunter le GAR
            if not is_gar_check and request.user.school.gar :
                request.session["is_gar_check"] = True
        except : 
            pass

        theme_color        =  'css/Admin_'+request.user.color+'.css'
        navbar_theme_color =  'css/navbar_'+request.user.color+'.css'

        sacado_asso = False
        if request.user.time_zone:
            time_zome = request.user.time_zone
            timezone.activate(pytz.timezone(time_zome))
            today = timezone.localtime(timezone.now())
        else:
            today = timezone.now()

        if request.user.is_teacher:

            dico_helper = { "/account/profile" : "profile" , "/account/avatar" : "avatar" , "/account/updatepassword" : "updatepassword" , "/school/get_school" : "get_school" ,  
                            "/" : "groupe" , "/#" : "groupe" ,  "/qcm/folders" : "folders" ,  "/qcm/parcours" : "parcours" ,  "/qcm/evaluations" : "evaluations" ,  "/qcm/evaluations" : "evaluations" ,  "qcm/parcours_my_courses" : "parcours_my_courses" , 
                            "/tool_list" : "quizzes" , "/bibliotex/my_bibliotexs" : "my_bibliotexs" ,  "/flashcard/my_flashpacks" : "my_flashpacks" ,  "/qcm/exercises" : "exercises" ,  "/tool/list_visiocopie" : "list_visiocopie" ,  
                            "/tool/list_tools" : "list_tools" , "/tool/show/" : "tool_show"  , "/sendmail/" : "sendmail" , "/aefe/" : "aefe" , "/admin_tdb" : "admin_tdb" ,"/qcm/parcours_group/" : "parcours_group",
                            "/qcm/parcours_sub_parcours/" : 'parcours_sub_parcours' , '/qcm/parcours_update/' : "parcours_update" , "/group/show/" :"group_show" , "/group/update/" : "group_update" , '/qcm/parcours_show/' :  'parcours_show',
                            "/school/groups" : 'school_groups' , '/school/new_student/' : 'school_new_student' , '/school/new_student_list/' : 'school_new_student_list'  }


            ihelp=0 
            request_path = str(request.path) 
            while ihelp < len(request_path) and not('0'<=request_path[ihelp]<='9' )    : ihelp+=1  
            helper_key = request_path[:ihelp] 
            try :
                url_helper = "helpers/" + dico_helper[helper_key] + ".html"
            except :
                url_helper = "helpers/no_helper.html"
 

            teacher = request.user.teacher

            nb_groups = teacher.groups.count()
            nb_levels = teacher.levels.count()
            #nbs = Studentanswer.objects.filter(parcours__teacher=teacher, date=today).count()
            nbe = Email.objects.values_list("id").distinct().filter(receivers=request.user, today=today).count()
            #nb_not = nbs + nbe
            levels = Level.objects.exclude(pk=13).order_by("ranking")
            nb_demand = Demand.objects.filter(done=0).count()

            mytools = Tool.objects.filter(is_publish=1, teachers = teacher).order_by("title")

            ### Exercice traités non vus par l'enseignant -> un point orange dans la barre de menu sur message
            is_pending_studentanswers = False
            pending_s = Studentanswer.objects.filter(parcours__teacher = teacher, is_reading = 0)
            if pending_s  :
                is_pending_studentanswers = True
 
            ### Permet de vérifier qu'un enseignant est dans un établissement sacado
            sacado_asso, sacado_is_active = is_sacado_asso(teacher.user,today)
 
            ### Rapelle le renouvellement de la cotisation
            renew_hidden = request.session.get("renewal", False)
            if not renew_hidden :
                rates = Rate.objects.all() #tarifs en vigueur 
                today = datetime.now()

                if Abonnement.objects.filter(school = teacher.user.school,   date_stop__gte=today, date_start__lte=today,is_active = 1 ).count() == 1:
                    renew_hidden = True
                    request.session["renewal"] = renew_hidden
            
            return { 'url_helper' : url_helper ,  'theme_color' : theme_color , 'navbar_theme_color' : navbar_theme_color , 'nb_levels' : nb_levels , 'nb_groups' : nb_groups ,  'is_gar_check' : is_gar_check,'today': today, 'index_tdb' : False , 'nbe': nbe, 'levels': levels, 'renew_propose' : renew_hidden ,  'nb_demand' : nb_demand , 'mytools' : mytools , 'sacado_asso' : sacado_asso , "is_pending_studentanswers" : is_pending_studentanswers  }

        elif request.user.is_student:
            
            student = Student.objects.get(user=request.user)
            groups = student.students_to_group.all()
 

            teacher_to_student = False
            if "_e-test" in student.user.username :
                teacher_to_student = True


            sacado_asso, sacado_is_active = is_sacado_asso(student.user,today)

            group_id = request.session.get("group_id",None)

            if group_id :
                group = Group.objects.get(pk=group_id)
            else :
                group = None

            url_helper =  "helpers/no_helper.html"

            return {
                'is_gar_check' : is_gar_check,
                'student': student,
                'sacado_asso' : sacado_asso , 
                'group' : group , 'url_helper' : url_helper ,
                'groups' : groups,
                'teacher_to_student' : teacher_to_student ,   
                'index_tdb' : False , 'theme_color' : theme_color , 'navbar_theme_color' : navbar_theme_color ,          
            }

        elif request.user.is_parent:
            this_user = User.objects.get(pk=request.user.id)
            students = this_user.parent.students.all()
            last_exercises_done = Studentanswer.objects.filter(student__in= students).order_by("-date")[:10]
            url_helper =  "helpers/no_helper.html"

            return {
                'this_user': this_user,
                'last_exercises_done': last_exercises_done,
                'sacado_asso' : sacado_asso , 
                 'sacado_asso' : False ,  'url_helper' : url_helper , 
                 'index_tdb' : False ,
                 'is_gar_check' : None, 'theme_color' : theme_color , 'navbar_theme_color' : navbar_theme_color ,
            }


    else:
 
 
 
        contributeurs = User.objects.filter(is_superuser=1)
 
 
        return {
 
            'contributeurs': contributeurs,
  
        }
