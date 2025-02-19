from django.db import models

from django.db import models
 
from account.models import Teacher
from bibliotex.models import    Exotex
from flashcard.models import Flashpack
from group.models import Group
from qcm.models import   Exercise , Parcours, Docperso
 
from socle.models import Level , Subject , Skill , Knowledge , Theme
from ckeditor_uploader.fields import RichTextUploadingField
 

def image_book_path(instance,filename):
    return "book/{}/{}".format(instance.id,filename)


def document_path(author,filename):
    return "chapter/{}/{}".format(author.user.id,filename)



class Book(models.Model):

    title         = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
    author        = models.ForeignKey(Teacher, on_delete=models.CASCADE,  blank=True,   related_name='author_books', verbose_name="Enseignant", editable= False)
    teachers      = models.ManyToManyField(Teacher, related_name="teacher_books", blank=True,  verbose_name="Participants", editable= False)
    level         = models.ForeignKey(Level, on_delete=models.CASCADE,  related_name='books', verbose_name="Niveau")
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE,  related_name='books', verbose_name="Enseignement")

    is_publish   = models.BooleanField(default=0, verbose_name="Publié ?")
    is_share     = models.BooleanField(default=0, verbose_name="Mutualisé ?")

    is_student    = models.BooleanField(default=0, verbose_name="Livre élève ?")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    texte         = models.TextField( null=True, blank=True,  verbose_name="Texte")      
    date_created  = models.DateTimeField( auto_now_add= True)
    groups        = models.ManyToManyField(Group, blank=True, related_name='books', verbose_name="Groupes")
    imagefile     = models.ImageField(upload_to=image_book_path, blank=True,  verbose_name="Fichier", default="")
    ranking       = models.PositiveIntegerField( default=0,  blank=True, null=True)
    price         = models.DecimalField( decimal_places=2, default=6, max_digits=4, blank=True, null=True) 

    color         = models.CharField(max_length=255, default="#5d4391" , blank=True, verbose_name="Couleur")
    color_hover   = models.CharField(max_length=255, default="#9274C7" , blank=True, verbose_name="Couleur hover")
 
    def __str__(self):
        return "{}".format(self.title)

    def total_page(self):
        i = 0
        for c in self.chapters.order_by("ranking") :
            for p in c.pages.order_by("number") :
                i+=1
        return i


class Chapter(models.Model):

    THEMES = (
        ("NC","Nombres et calculs"),
        ("G", "Géométrie"),
        ("F", "Fonctions"),
        ("SP","Statistiques et probabilités"),
        ("GM","Grandeurs et Mesures"),
        ("A", "Algèbre"),
        ("OGD", "Organisation et Gestion de données"),
        ("AP", "Algorithme et programmation"),
    )
 
    title         = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")

    author        = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='author_chapters', blank=True,null=True,  verbose_name="Enseignant")
    teacher       = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="teacher_chapters", blank=True,null=True,  verbose_name="Participants")

    theme         = models.CharField(max_length=255, null=True, blank=True, choices=THEMES ,  verbose_name="Thème")

    is_publish    = models.BooleanField(default=0, verbose_name="Publié ?")
    is_share      = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_progression = models.BooleanField(default=1, verbose_name="Dans ma progression ?")
    ranking       = models.PositiveIntegerField( default=0,  blank=True, null=True)

    date_created  = models.DateTimeField( auto_now_add= True)
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    book          = models.ForeignKey(Book, on_delete=models.CASCADE,  blank=True,   related_name='chapters', editable=False)
    parcours      = models.ForeignKey(Parcours, on_delete=models.CASCADE , blank=True, null= True, related_name="chapters")
    flashpack     = models.ForeignKey(Flashpack, on_delete=models.CASCADE , blank=True, null= True, related_name="chapters", editable=False)  

    def __str__(self):
        return "{}".format(self.title)


    def is_correction(self,group):
        test = False
        for page in self.pages.all():
            for paragraph in page.paragraphs.all():
                for bloc in paragraph.blocs.all():
                    nb_myblocs = bloc.myblocs.values_list("id", flat=True).filter(group=group,is_display_cor=1).count()
                    if nb_myblocs > 0 : 
                        test = True
                        break
        return test


    def is_complement(self,group):
        test = False
        for page in self.pages.all():
            for paragraph in page.paragraphs.all():
                for bloc in paragraph.blocs.all():
                    nb_myblocs = bloc.myblocs.values_list("id", flat=True).filter(group=group,is_display_comp=1).count()
                    if nb_myblocs > 0 : 
                        test = True
                        break
        return test


class Section(models.Model):

    title      = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
    ranking    = models.PositiveIntegerField( default=0)
    chapter    = models.ForeignKey(Chapter, on_delete=models.CASCADE,  blank=True, null=True,  related_name='sections', editable=False)
    color      = models.CharField(max_length=15, null=True, blank=True, default="#9274C7",   verbose_name="Couleur")
    is_publish = models.BooleanField(default=1, blank=True  )

    def __str__(self):
        return "{}".format(self.title )

    class Meta:
        unique_together = ('title', 'chapter')

##################################     doctypes     ################################################    
##  doctypes  ["content","file","url","GGB","Quizz","Course","BiblioTex","Exotex","flashpack","QF","DocPerso"]
##  doc_id    [    0    ,   1  ,  2  ,  3  ,   4   ,   5    ,     6     ,   7    ,      8    ,  9 ,   10     ]
##################################     doctypes     ################################################

class Document(models.Model):
 
    title    = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
    section  = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True, related_name='documents', verbose_name="Section")

    author   = models.ForeignKey(Teacher, on_delete=models.CASCADE,  blank=True,null=True, related_name='author_documents', verbose_name="Auteur")
    teacher  = models.ForeignKey(Teacher, on_delete=models.CASCADE,  blank=True,null=True, related_name="documents", verbose_name="Participants")

    level    = models.ForeignKey(Level, on_delete=models.CASCADE,  blank=True,null=True,  related_name='documents', verbose_name="Niveau")
    subject  = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True, related_name='documents', verbose_name="Enseignement")
    ranking  = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)

    content  = RichTextUploadingField( blank=True,  verbose_name="Texte")  
    file     = models.FileField(upload_to=document_path, blank=True,  verbose_name="Fichier", default="")
    url      = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Lien externe")

    doctype  = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)#doctypes = ["content","file","url","exercise","quizz","question","bibliotex","exotex","flashcard","flashpack"]
    doc_id   = models.PositiveIntegerField( default=0,  blank=True, null=True, editable=False)

    is_publish   = models.BooleanField(default=0, verbose_name="Publié ?")
    is_share     = models.BooleanField(default=0, verbose_name="Mutualisé ?")
    is_done = models.BooleanField(default=0, blank=True, null=True, verbose_name="Effectué ?")
    
    def __str__(self):
        return "{} {}".format(self.title,self.level.name)

    def icon_doctype(self):
        doc_url = ""
        doc_support_id = self.doc_id
        if self.doctype == 0 : 
            icon = '<i class="bi bi-file-earmark book_main_page_section_document_earmark"></i>'
            doc_url = "show_this_exercise"
        elif self.doctype == 1 : 
            icon = '<i class="bi bi-file book_main_page_section_document_earmark"></i>'
            doc_url = self.file
        elif self.doctype == 2 : 
            icon = '<i class="bi bi-link  book_main_page_section_document_earmark"></i>'
            doc_url = self.url
        elif self.doctype == 3 : 
            exercise = Exercise.objects.get(pk=self.doc_id)
            try :
                icon = "<img src='"+exercise.supportfile.imagefile.url+"' class='mini_imagefile' />"
            except :
                icon = '<i class="bi bi-explicit  book_main_page_section_document_earmark"></i>'
            if exercise.supportfile.is_ggbfile :
                doc_url = "show_this_exercise"
            else :
                doc_url = "show_all_type_exercise"
                doc_support_id = exercise.supportfile.id
        elif self.doctype == 4 : #quiz
            icon = '<i class="bi bi-file-aspect-ratio  book_main_page_section_document_earmark"></i>'
            doc_url = "show_quizz"
        elif self.doctype == 5 :
            icon = '<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-c-square" viewBox="0 0 16 16"><path d="M8.146 4.992c-1.212 0-1.927.92-1.927 2.502v1.06c0 1.571.703 2.462 1.927 2.462.979 0 1.641-.586 1.729-1.418h1.295v.093c-.1 1.448-1.354 2.467-3.03 2.467-2.091 0-3.269-1.336-3.269-3.603V7.482c0-2.261 1.201-3.638 3.27-3.638 1.681 0 2.935 1.054 3.029 2.572v.088H9.875c-.088-.879-.768-1.512-1.729-1.512Z"/><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2Zm15 0a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V2Z"/></svg>'
            doc_url = "show_one_course"
        elif self.doctype == 6 : 
            icon = '<i class="bi bi-bootstrap  book_main_page_section_document_earmark"></i>'
            doc_url = "show_bibliotex"
        elif self.doctype == 7 : 
            icon = '<i class="bi bi-explicit  book_main_page_section_document_earmark"></i>'
            doc_url = "show_exotex"
        elif self.doctype == 8 : 
            icon = '<i class="bi bi-stack  book_main_page_section_document_earmark"></i>'
            doc_url = "show_flashpack"
        elif self.doctype == 9 : 
            icon = '<i class="bi bi-lightning  book_main_page_section_document_earmark"></i>'
            doc_url = "show_questions_flash"
        elif self.doctype == 10 : 
            icon = '<i class="bi bi-file  book_main_page_section_document_earmark"></i>'
            docu = Docperso.objects.get(pk=self.doc_id)
            if docu.link : doc_url = docu.link
            else : doc_url = docu.file.url
        data = {}
        data["icon"] = icon
        data["url"] = doc_url
        data["support_id"] = doc_support_id
        return data




 

class Documentex(models.Model):

    exotex = models.ForeignKey(Exotex,  on_delete=models.CASCADE,   related_name='documentexs', editable= False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE,  related_name='documentexs',  editable= False)
    content = models.TextField( null=True, blank=True, verbose_name="Enoncé en LaTeX")
    content_html = models.TextField( null=True, blank=True)    

    correction = models.TextField( blank=True, default="", null=True, verbose_name="Correction en LaTeX")
    correction_html = models.TextField( blank=True, default="", null=True) 
    is_publish_cor = models.BooleanField(default=0, verbose_name="Publié ?") 

    #### pour validation si le qcm est noté
    calculator = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    #### pour donner une date de remise
 
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
 
    duration = models.PositiveIntegerField(default=15, blank=True, verbose_name="Durée estimée - en minutes")

    author  = models.ForeignKey(Teacher, on_delete=models.CASCADE,  related_name='author_chapterxtexs', verbose_name="Enseignant")
    teacher = models.ManyToManyField(Teacher, related_name="teacher_chapterxtexs", blank=True,  verbose_name="Participants")

    ###### Socle
    skills = models.ManyToManyField(Skill, blank=True, related_name='documentexs', verbose_name="Compétences ciblées")
    knowledges = models.ManyToManyField(Knowledge, related_name='documentexs', verbose_name="Savoir faire associés complémentaires")

    is_python = models.BooleanField(default=0, verbose_name="Python ?")
    is_scratch = models.BooleanField(default=0, verbose_name="Scratch ?")
    is_tableur = models.BooleanField(default=0, verbose_name="Tableur ?")
    is_print = models.BooleanField(default=0, verbose_name="Imprimé ?")
    is_publish = models.BooleanField(default=0, verbose_name="Publié ?")
    start = models.DateTimeField(null=True, blank=True, verbose_name="A partir de")
    stop = models.DateTimeField(null=True, blank=True, verbose_name="Date de verrouillage")

    ranking = models.PositiveIntegerField(  default=0,  blank=True, null=True, editable=False)
    point = models.PositiveIntegerField(  default=0,  blank=True, null=True ,  verbose_name="Points") 



    def __str__(self):       
        return "{} > {}".format(self.chapter.title,self.document.title)

    class Meta:
        unique_together = ('exotex', 'document')


################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
###############################################               LIVRET ELEVE             #########################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################

class Page(models.Model):

    title   = models.CharField(max_length=255, default="Cours" , blank=True,   verbose_name="Titre de la page")
    number  = models.PositiveIntegerField( default=0,  blank=True, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,  blank=True,   null=True,  related_name='pages')
    css     = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Nom de la classe")
    is_publish = models.BooleanField(default=1, verbose_name="Publiée ?")

    # class Meta:
    #     unique_together = ('number', 'chapter')


    def __str__(self):
        return "{} : {}".format(self.number,self.title)

    def is_correction(self,group):
        test = False
        for paragraph in self.paragraphs.all():
            for bloc in paragraph.blocs.all():
                nb_myblocs = bloc.myblocs.values_list("id", flat=True).filter(group=group,is_display_cor=1).count()
                if  nb_myblocs  > 0 : 
                    test = True
                    break
        return test

    def is_complement(self,group):
        test = False
        for paragraph in self.paragraphs.all():
            for bloc in paragraph.blocs.all():
                nb_myblocs = bloc.myblocs.values_list("id", flat=True).filter(group=group,is_display_comp=1).count()
                if  nb_myblocs  > 0 : 
                    test = True
                    break
        return test
    

    def body_css(self) :
        if self.css == 'parcoursu_page_top' : return 'course_page_u_main'
        elif self.css == 'parcoursd_page_top' : return 'course_page_d_main'
        elif self.css == 'parcourst_page_top' : return 'course_page_t_main'
        elif self.css == 'ad_page_top' : return 'course_page_ad_main'
        elif self.css == 'auto_page_top' : return 'course_page_a_main'
        elif self.css == 'algo_page_top' : return 'course_page_al_main'
        else :  return ''









class Paragraph(models.Model):

    page    = models.ForeignKey(Page, on_delete=models.CASCADE,  blank=True, null=True,  related_name='paragraphs')
    title   = models.CharField(max_length=255,     verbose_name="Titre")
    number  = models.PositiveIntegerField( default=1 )
    ranking = models.PositiveIntegerField( default=0, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.title )



    def col_width(self,loop):
        nb = 0
        for b in self.blocs.values_list("size",flat=True).order_by("ranking")[:loop]:
            nb += b
        return nb




    def total_size(self):
        nb = 0
        for b in self.blocs.values_list("size",flat=True).order_by("ranking"):
            nb += b
        return nb


    def is_correction(self,group):
        test = False
        for bloc in self.blocs.all():
            nb_myblocs = bloc.myblocs.values_list("id", flat=True).filter(group=group,is_display_cor=1).count()
            if nb_myblocs > 0 : 
                test = True
                break
        return test


    def is_complement(self,group):
        test = False
        for bloc in self.blocs.all():
            nb_myblocs = bloc.myblocs.values_list("id", flat=True).filter(group=group,is_display_comp=1).count()
            if nb_myblocs > 0 : 
                test = True
                break
        return test
##################################     doctypes     ################################################    
##  doctypes  ["définition","Exemple","url","GGB","Quizz","Course","BiblioTex","Exotex","flashpack","QF"]
##  doc_id    [    0    ,   1  ,  2  ,  3  ,   4   ,   5    ,     6     ,   7    ,      8    ,  9 ]
##################################     doctypes     ################################################

class Typebloc(models.Model):

    title     = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
    css       = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Nom de la classe")
    latexbloc = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Latex Bloc")
    latextype = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Latex type")


    def __str__(self):
        return "{}".format(self.title )





class Appliquette(models.Model):


    forme    = models.CharField(max_length=255,  default="", verbose_name="Forme")
    title    = models.CharField(max_length=255,  default="", verbose_name="Titre")
    url      = models.CharField(max_length=255,  default="", verbose_name="url")
    iframe   = models.TextField( verbose_name="Iframe")
    level    = models.ForeignKey(Level, on_delete=models.CASCADE, default="", blank=True, related_name='appliquettes', verbose_name="Niveau")
    code     = models.CharField(max_length=255,  default="",  blank=True, verbose_name="code")

    def __str__(self):
        return "{} > {}".format(self.code,self.title)




class Bloc(models.Model):

    SIZES = (
        (12,"Page entière"),
        (10, "5/6 page"),
        (9, "3/4 page"),
        (8, "2/3 page"),
        (7, "7/12 page"),    
        (6, "1/2 page"),
        (5, "5/12 page"),   
        (4, "1/3 page"),
        (3, "1/4 page"),
        (2, "1/6 page"),
    )


    title     = models.CharField(max_length=255, null=True, blank=True,   verbose_name="Titre")
    typebloc  = models.ForeignKey(Typebloc, on_delete=models.CASCADE, related_name='blocs', verbose_name="Type de bloc")
    paragraph = models.ForeignKey(Paragraph, on_delete=models.CASCADE, related_name='blocs')
    ranking   = models.PositiveIntegerField( default=0,  blank=True, null=True)

    size       = models.PositiveSmallIntegerField(choices=SIZES, default=12, blank=True, verbose_name="Colonne")

    content         = models.TextField( blank=True,  verbose_name="Enoncé en LaTeX")
    content_html    = RichTextUploadingField( blank=True,   verbose_name="Enoncé pour html") 
    correction      = models.TextField( blank=True, default="", null=True, verbose_name="Corrigé")
    correction_html = RichTextUploadingField( blank=True,  verbose_name="Correction pour html")
    is_correction   = models.BooleanField(default=0, editable=False)  
    #### pour validation si le qcm est noté

    duration = models.PositiveIntegerField(default=15, blank=True, verbose_name="Durée estimée - en minutes")

    ###### Socle
    knowledge  = models.ForeignKey(Knowledge,  on_delete=models.CASCADE,  blank=True, null=True,    related_name='blocs', verbose_name="Savoir faire associé")
    theme      = models.ForeignKey(Theme,      on_delete=models.CASCADE,  blank=True, null=True ,   related_name="blocs",  verbose_name="Thème")
    skills     = models.ManyToManyField(Skill, blank=True, related_name='blocs', verbose_name="Compétences ciblées")
    knowledges = models.ManyToManyField(Knowledge, blank=True,  related_name='other_knowledge_blocs', verbose_name="Savoir faire associés complémentaires")
    
    is_calculator = models.BooleanField(default=0, verbose_name="Calculatrice ?")
    is_python    = models.BooleanField(default=0, verbose_name="Python ?")
    is_scratch   = models.BooleanField(default=0, verbose_name="Scratch ?")
    is_tableur   = models.BooleanField(default=0, verbose_name="Tableur ?")
    is_corrected = models.BooleanField(default=0, verbose_name="Correction ?")
    is_annals    = models.BooleanField(default=0, verbose_name="Annale ?")

    insidebloc   = models.ForeignKey('self',  on_delete=models.CASCADE,  blank=True, null=True,   verbose_name="Dans le bloc")

    exercises    = models.ManyToManyField(Exercise, blank=True, related_name='blocs', verbose_name="Exercices connexes")
    exotexs      = models.ManyToManyField(Exotex  , blank=True, related_name='blocs', verbose_name="ExoTex connexes")
    appliquettes = models.ManyToManyField(Appliquette, blank=True, related_name='blocs', verbose_name="Appliquettes")



    def __str__(self):
        return "{} > {}".format(self.title,self.typebloc.title)


    def display_qr(self):
        return self.exercises.count() or self.exotexs.count() or self.appliquettes.count() or self.correction_html


    def typebloc_latex(self):

        try :
            suffixe = self.typebloc.css.split("_")[2] + "T"
        except :
            suffixe = "exoT"
        suffixe = self.typebloc.css.split("_")[2] + "T"

        try : splitter = self.title.split(".")
        except : 
            if self.title == "" : splitter = ["",""]
            else : splitter = self.title

        details = ""
        if self.correction :
            details += r" \href{https://sacado.xyz/c/"+str(self.id)+r"}{C.} "
        for e in self.exercises.all() :
            details +=  r" \href{https://sacado.xyz/qcm/show_exercise_to_tex/"+str(e.supportfile.code)+r"}{"+str(e.supportfile.code)+r"} - "
        for e in self.exotexs.all() :
            details +=  r" \href{https://sacado.xyz/bibliotex/exercise_exotex_show/"+str(e.id)+r"}{"+str(e.id)+r"} - "
        for a in self.appliquettes.all() :
            details +=  r" \href{https://sacado.xyz/a/"+str(a.code)+r"}{"+str(a.code)+r"} - "

        if splitter and len(splitter)>1 : stringer = r" \begin{GeneriqueT}{"+splitter[0]+r"}{"+splitter[1]+" "+details+" "+ r"}"+self.content+r"\end{GeneriqueT} "
        elif not splitter : stringer = r" \begin{GeneriqueT}{}{"+details+r"}"+self.content+r"\end{GeneriqueT} "
        else : stringer = r" \begin{GeneriqueT}{"+self.title+r"}{"+details+r"}"+self.content+r"\end{GeneriqueT} "

        #return r"\begin{"+suffixe+r"}{"+self.title+r"}"+self.content+r"\end{"+suffixe+r"}"
        return stringer

    def css(self) :
        if self.paragraph.page.css == 'parcoursu_page_top' : return 'exo_u'
        elif self.paragraph.page.css == 'parcoursd_page_top' : return 'exo_d'
        elif self.paragraph.page.css == 'parcourst_page_top' : return 'exo_t'
        elif self.paragraph.page.css == 'parcourst_page_top' : return 'exo_auto'
        else :  return ''


    def bloc_css(self) :
        if self.paragraph.page.css == 'parcoursu_page_top' : return 'exo_bloc_u'
        elif self.paragraph.page.css == 'parcoursd_page_top' : return 'exo_bloc_d'
        elif self.paragraph.page.css == 'parcourst_page_top' : return 'exo_bloc_t'
        elif self.paragraph.page.css == 'parcourst_page_top' : return 'exo_bloc_auto'
        else :  return ''


    def is_correction(self,group):
        test = False
        nb_myblocs = self.myblocs.values_list("id", flat=True).filter(group=group,is_display_cor=1).count()
        if nb_myblocs > 0 : 
            test = True
        return test

    def is_complement(self,group):
        test = False
        nb_myblocs = self.myblocs.values_list("id", flat=True).filter(group=group,is_display_comp=1).count()
        if nb_myblocs > 0 : 
            test = True
        return test    

    def bloc_cor_visible_by_student(self, groups) :
        test = False
        for group in groups :
            nb_myblocs = self.myblocs.filter(group=group,is_display_cor=1).count()
            if nb_myblocs > 0 : 
                test = True
                break
        return test   

    def bloc_comp_visible_by_student(self, groups) :
        test = False
        for group in groups :
            nb_myblocs = self.myblocs.filter(group=group,is_display_comp=1).count()
            if nb_myblocs > 0 : 
                test = True
                break
        return test  







###############################################################################################################
############################## Attribution d'un livre à un groupe #############################################
###############################################################################################################

class Mybook(models.Model):

    group      = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="mybooks", blank=True,null=True,  verbose_name="Groupe")
    book       = models.ForeignKey(Book, on_delete=models.CASCADE,  blank=True,   related_name='mybooks', editable=False)
    is_display = models.BooleanField(default=0, verbose_name="Publié ?")


    def __str__(self):
        return "{} > {}".format(self.group.name,self.book.title)


class Mybloc(models.Model):
    group           = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="myblocs", blank=True,null=True,  verbose_name="Groupe")
    bloc            = models.ForeignKey(Bloc, on_delete=models.CASCADE,  blank=True,   related_name='myblocs', editable=False)
    is_display_cor  = models.BooleanField(default=0, verbose_name="Publié ?")
    is_display_comp = models.BooleanField(default=1, verbose_name="Publié ?")

    def __str__(self):
        return "{} > {} > {}".format(self.group.name,self.bloc.title,self.is_display_cor)


  