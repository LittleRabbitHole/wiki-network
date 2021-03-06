#from django.db import models
from django.db.models import *
from fields import DictionaryField


class WikiRunData(Model):
    lang = CharField(max_length=3, blank=False)
    date = CharField(max_length=8, blank=False)

    # --details
    nodes_number = IntegerField(blank=True, null=True)
    edges_number = IntegerField(blank=True, null=True)
    nodes_with_out_edges_number = IntegerField(blank=True, null=True)
    nodes_with_in_edges_number = IntegerField(blank=True, null=True)
    max_weights_on_edges = CharField(max_length=100, blank=True, null=True)
    reciprocity = FloatField(blank=True, null=True)
    #average_weight = FloatField(blank=True, null=True)

    # --density
    density = FloatField(blank=True, null=True)

    length_of_5_max_clusters = CharField(max_length=100, blank=True, null=True)

    # --distance
    average_distance_in_the_giant_component = FloatField(blank=True, null=True)
    average_hops_in_the_giant_component = FloatField(blank=True, null=True)

    # --efficiency
    efficiency = FloatField(blank=True, null=True)

    # --power-law
    alpha_exp_of_the_power_law = FloatField(blank=True, null=True)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s, %s" % (self.lang, self.date)


class WikiRunGroupData(Model):
    wikirun = ForeignKey(WikiRunData)
    lang = CharField(max_length=3, blank=False)
    date = CharField(max_length=8, blank=False)
    group = CharField(max_length=20, blank=False)
    nodes_number = IntegerField(blank=True, null=True)

    # --degree
    mean_IN_degree_no_weights = FloatField(blank=True, null=True)
    mean_OUT_degree_no_weights = FloatField(blank=True, null=True)
    max_IN_degrees_no_weights = CharField(max_length=100, blank=True)
    max_OUT_degrees_no_weights = CharField(max_length=100, blank=True)
    stddev_IN_degree_no_weights = FloatField(blank=True, null=True)
    stddev_OUT_degree_no_weights = FloatField(blank=True, null=True)

    # --density
    density = FloatField(blank=True, null=True)

    # --reciprocity
    reciprocity = FloatField(blank=True, null=True)

    # --centrality
    average_betweenness = FloatField(blank=True, null=True)
    stddev_betweenness = FloatField(blank=True, null=True)
    max_betweenness = CharField(max_length=100, blank=True)

    average_pagerank = FloatField(blank=True, null=True)
    stddev_pagerank = FloatField(blank=True, null=True)
    max_pagerank = CharField(max_length=100, blank=True)

    average_IN_degree_centrality_weighted = FloatField(blank=True, null=True)
    stddev_IN_degree_centrality_weighted = FloatField(blank=True, null=True)
    max_IN_degrees_centrality_weighted = CharField(max_length=100, blank=True)

    average_OUT_degree_centrality_weighted = FloatField(blank=True, null=True)
    stddev_OUT_degree_centrality_weighted = FloatField(blank=True, null=True)
    max_OUT_degrees_centrality_weighted = CharField(max_length=100, blank=True)

    # --power-law
    alpha_exp_IN_degree_distribution = FloatField(blank=True, null=True)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s-%s created on: %s" % (self.lang, self.date,
                                          self.created.isoformat())


class WikiStat(Model):
    ## name
    lang = CharField(max_length=20, blank=False)
    family = CharField(max_length=20, blank=False, default="wikipedia")

    ## data
    articles = IntegerField(blank=True, null=True)
    jobs = IntegerField(blank=True, null=True)
    users = IntegerField(blank=True, null=True)
    admins = IntegerField(blank=True, null=True)
    edits = IntegerField(blank=True, null=True)
    activeusers = IntegerField(blank=True, null=True)
    images = IntegerField(blank=True, null=True)
    pages = IntegerField(blank=True, null=True)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s, stats of %s" % (self.lang, self.created.isoformat())


class WikiLang(Model):
    lang = CharField(max_length=20, primary_key=True)

    lang_group = CharField(max_length=20, blank=True, null=True)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.lang


class BigWikiStat(Model):
    rank = IntegerField(blank=True, null=True)
    _id = IntegerField(blank=True, null=True)
    name = CharField(max_length=200)
    total = IntegerField(blank=True, null=True)
    good = IntegerField(blank=True, null=True)
    edits = IntegerField(blank=True, null=True)
    views = IntegerField(blank=True, null=True)
    admins = IntegerField(blank=True, null=True)
    users = IntegerField(blank=True, null=True)
    activeusers = IntegerField(blank=True, null=True)
    images = IntegerField(blank=True, null=True)
    ratio = FloatField(blank=True, null=True)
    type = CharField(max_length=50, blank=True, null=True)
    url = CharField(max_length=200, blank=True, null=True)
    ts = DateTimeField()

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)


class CeleryRun(Model):
    #celery related
    name = CharField(max_length=36)
    hide = BooleanField(default=False)

    #wiki related
    lang = CharField(max_length=20, blank=False)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)


class WikiPage(Model):
    """
    Abstract Model to store generic information about a Wikipedia Page (article
    or talk page)
    """
    title = TextField(db_index=True)
    lang = CharField(max_length=7, db_index=True)
    talk = BooleanField(default=False)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s: %s" % (self.lang, self.title)

    def get_absolute_url(self):
        return "http://%(lang)s.wikipedia.org/wiki/%(talk)s%(title)s" % {
            'lang': self.lang,
            'title': self.title,
            'talk': 'Talk:' if self.talk else ''
        }


class WikiEvent(WikiPage):
    """
        Model used to store revisions per date per page in wiki history dump.
         * desired is used as a flag for internal use
         * talk tells us if this is a talk or a normal page
         * total_editors: number of unique total editors
         * bot_editors: number of unique bot editors
         * anonymous_editors: number of unique anonymous editors

        If you use postgresql, execute
        CREATE INDEX wikinetwork_wikievent_title_talk_LANG ON
            wikinetwork_wikievent (title, talk) WHERE lang='LANG';
        and replace LANG with every language you want to store
        (eg.: en, it, de)
    """

    desired = BooleanField(default=False)
    data = DictionaryField()
    total_editors = IntegerField(blank=True, null=True)
    bot_editors = IntegerField(blank=True, null=True)
    anonymous_editors = IntegerField(blank=True, null=True)


class WikiWord(WikiPage):
    desired = BooleanField(default=False)
    data = DictionaryField(null=True)
    data_first = DictionaryField(null=True)
