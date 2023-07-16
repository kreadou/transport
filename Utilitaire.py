# -*- coding:utf-8 -*-
from itertools import *
from collections import *
import datetime, time
import sys, os

lesMois=('Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec')

#utils.py
#from django.db.models import Count, Sum

### pour exploiter les milliers et decimaux
def floatChaine(valeur, separateur = ' ', point = '.', decimal = 2):
    if valeur:
        c = str(valeur)
        if '.' in c:
            q, z = c[:c.index('.')], c[c.index('.')+1:]
            
            z = z[:decimal]
            print('dec =', decimal==True)
            if decimal:
                return millier(q)+point+z+''.join(['0' for s in range(decimal-len(z))])
            else:return millier(q)
        elif ',' in c:
            q, z = c[:c.index(',')], c[c.index(',')+1:]
            z = z[:decimal]
            if decimal:return millier(q)+point+z+''.join(['0' for s in range(decimal-len(z))])
            else:return millier(q)
        elif c.isdigit():
            return millier(int(c))
        else: return valeur
    return valeur


def get_total_per_month_value():
    #Return the total of sales per month
    #ReturnType: [Dict]
    #{'December': 3400, 'February': 224, 'January': 792}
    
    result= {}
    db_result = Opportunite.objects.values('montantEstime','dateCreation')
    for i in db_result:
        month = str(i.get('dateCreation').strftime("%B"))
        if month in result.keys():
            result[month] = result[month] + i.get('montantEstime')
        else:
            result[month] = i.get('montantEstime')
    return result


def ouvrirPDF(fichier=None):
    try:
        os.startfile(fichier)
    except:pass
    return True


""" il nettoie les tableau en reglant les decimaux à 2 chiffres """
def nettoieFloat(t=None):
    if t:return partagerListe(map(lambda x : '%.2f'%x if type(x) in (type(0.2),) else x, aplatliste(t)), len(t))
    else:return t


def Appreciation(t=None):
    return map(lambda x:iif(x in ('nc',None,''),'nc',iif(x<=8.5,u'Faible',\
    iif(8.5<x<10,u'Insuffisant',iif(10<=x<11,u'Passable',iif(11<=x<12,u'Moyen',\
    iif(12<=x<14,u'Assez bien',iif(14<=x<17,u'Bien',iif(17<=x<18,u'Très bien',u'Excellent')))))))),t)


def Resultat(t=None):
    return map(lambda x:iif(x in ('nc',None,''),'Ajourné',iif(x<=8.5,u'Ajourné',\
    iif(8.5<x<10,u'Ajourné',iif(10<=x<11,u'Validé',iif(11<=x<12,u'Validé',\
    iif(12<=x<14,u'Validé',iif(14<=x<17,u'Validé',iif(17<=x<18,u'Validé',u'Validé')))))))),t)


def supprimerColonneListe(t=None, n=0):
    try:
        return zip(*zip(*t)[:n]+zip(*t)[n+1:])
    except:return t


def sumAmelioree(t=None):
    if t:
        if type(t) in (type((5,7,4)), type([5,7,4])):
            try:
                return sum([ i for i in t if type(i) in (type(1), type(0.2))])
            except:return 0
        return 0
    return 0


def largeurColonne(t=None, n=5.8):
    if t:#=['kre adou joachim', 'dali yohou moise', 'coulibaly siaka']
        try:
            q=map(lambda x:tuple(x.split(' ')),t)
            #print 'split = ',q
            z=map(lambda x:[len(s) for s in x],q)
            #print 'split valeur = ',z
            #[[3, 4, 7], [4, 5, 6], [4, 5, 5], [9, 5]]
            w=map(lambda x:max([len(s) for s in x]),q)
            #print 'split max = ',w
            #print 'deja multi ', map(lambda x:max([len(s)*n for s in x]),q)
            return map(lambda x:max([len(s)*n for s in x]),q)
            #[7, 6, 5, 9]
        except:pass


def dateDuJour():
    temps=time.localtime()
    return str(temps[2])+'/'+str(temps[1])+'/'+str(temps[0])
"""
def jourSuivant(self, datex=dateDuJour(), nbreJour=1):
    p=tuple([(int(i))for i in datex.split('/')])
    datefin=datetime.date(p[2], p[1], p[0]) + datetime.timedelta(days=nbreJour)
    p=str(datefin).split('-')
    datefin=p[2]+'/'+p[1]+'/'+p[0]
    return datefin
"""

def numjoursem(D):
    """numjoursem(D): donne le numéro du jour de la semaine d'une date D 'j/m/a' (lundi=1, ...)"""
    L=D.split('/')
    an=int(L[2])-1
    j=(an+(an//4)-(an//100)+(an//400)+numjouran(D)) % 7
    if j==0: j=7
    return j
 

def joursem(D):
    """joursem(D): donne le jour de la semaine d'une date D 'j/m/a' ('lundi' pour lundi, ...)"""
    return ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche')[numjoursem(D)-1]


def nbjoursan(a):
    """Donne le nombre de jours de l'année"""
    if (a%4==0 and a%100!=0) or a%400==0: # bissextile?
        return 366
    else:
        return 365


def numjouran(d):
    d=str(d)
    """Donne le numéro du jour dans l'année de la date d=[j,m,a] (1er janvier = 1, ...)"""
    #print 'd = ',d, type(d)
    d=map(lambda x: int(x), d.split('/'))
    j, m, a = d
    if ((a%4==0 and a%100!=0) or a%400==0):  # bissextile?
        return (0,31,60,91,121,152,182,213,244,274,305,335,366)[m-1] + j
    else:
        return (0,31,59,90,120,151,181,212,243,273,304,334,365)[m-1] + j


def datenumjouran(n,a):
    """Donne la date d=[j,m,a] qui est le nième jour de l'année a"""
    if ((a%4==0 and a%100!=0) or a%400==0):  # bissextile?
        jm = (0,31,60,91,121,152,182,213,244,274,305,335,366)
    else:
        jm = (0,31,59,90,120,151,181,212,243,273,304,334,365)
    for m in range(1,13):
        if jm[m]>=n:
            return [n-jm[m-1], m, a]


def adddate(D,n):
    """adddate(D,n): donne la date postérieure de n jours (n>=0) ou antérieure de n jours (n<0) à la date D 'j/m/a'"""
    L=D.split('/')
    ak=int(L[2])
    if n>=0:
        nk=numjouran(D)+n
        while nk>nbjoursan(ak):
            nk=nk-nbjoursan(ak)
            ak=ak+1
        return datenumjouran(nk,ak)
    else:
        nk=abs(n)+nbjoursan(ak)-numjouran(D)
        while nk>=nbjoursan(ak):
            nk=nk-nbjoursan(ak)
            ak=ak-1
        return datenumjouran(nbjoursan(ak)-nk,ak)


def lundi(D):
    """lundi(D): trouve la date du lundi d'une semaine qui contient la date D 'j/m/a'"""
    x=adddate(D,-numjoursem(D)+1)
    return str(x[0])+'/'+str(x[1])+'/'+str(x[2])


class Etiquette(object):
    def __init__(self, parent=None):
        self.lab=QLabel()
        self.lab.setFrameShape(QFrame.Panel)
        self.lab.setFrameShadow(QFrame.Sunken)
    
    def creer(self, text=u''):
        self.lab.setText(u'{0}'.format(text))
        return self.lab

def compterOccurencePosition(t=None):
    if t:
        x=[]
        for i in t:
            if 1 < t.count(i):
                x.append((i, t.index(i), t.count(i)))
        x=list(set(x))
        x.sort()       
        return x
    else:return []

""" Alternative de la fonction utilisée dans Edts pour afficher Matière, Enseignant, Salle \
à l'impression de façon propre """
def reduireChaine(qq=None, longText=35):
    gg=""
    w=""
    pp=""
    if not qq:return ''
    m=qq[:]
    if len(m)>longText:
        save=""
        zz=m.split(" ")
        racine = zz[0]
        del zz[0]
        #print "zz = ",zz
        if zz:
            for v in range(len(zz)):
                if zz[-1]!='':
                    save=zz.pop(-1)[0]+ '. '+save
                    #print 'sauve = ',save
                else:zz.pop(-1)
                pp=(sumStr(zz[:])+" "+save).strip()
                #print 'pp = ', pp
                if not len(racine+' '+pp)>longText:break
                #print "racine + pp ",racine+' '+pp
            w=racine+' '+pp
        else:w=racine
    else:w+=m
    gg+=w+'\n'
    return gg[:-1]

""" cette fonction est utilisée dans Edts pour afficher Matière, Enseignant, Salle \
à l'impression de façon propre """
def reduireText(qq=None, longText=12):
    gg=""
    if len(qq):
        for h in qq:
            w=""
            pp=""
            m=h
            if len(m)>longText:
                save=""
                zz=m.split(" ")
                racine = zz[0]
                del zz[0]
                if zz:
                    for v in range(len(zz)):
                        if zz[-1]!='':save=zz.pop(-1)[0]+ '. '+save
                        else:zz.pop(-1)
                        pp=(sumStr(zz[:])+" "+save).strip()
                        if not len(racine+' '+pp)>longText:break
                    w=racine+' '+pp
                else:w=racine
            else:w+=m
            gg+=w+'\n'
    else:print("final vide")
    """ on enlève le retour chariot """
    return gg[:-1]


def sumStr(t=None):
    z=""
    if t:
        for j in t:z+=j+" "
        return z.strip()
    return ""
""" fin pour impression """

def compterOccurence(t=None):
    if t:
        x=[]
        y=[]
        z=[]
        for i in t:
            if i not in x:
                x.append(i)
                y.append((i, t.count(i)))
                print(u"le nombre de {0} est {1}".format(i, t.count(i)))
                if t.count(i)==1:
                    z.append(i)
        #y.sort(reverse = True)        
        return y
    print('la liste est vide')
#q,z=compterOccurence([10,25,3,10,4,8,4])
#print(q, '  ',z)

class OrderedDict(object):
    """A dictionary that is ordered by key
    
    Initializing with a dictionary is expensive because all the
    dictionary's keys must be sorted. This is also true of the update()
    method.
    """

    def __init__(self, dictionary=None):
        """Initializes with a shallow copy of the given dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        >>> OrderedDict()
        OrderedDict({})
        >>> e = OrderedDict(d)
        >>> e.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        self.__keys = []
        self.__dict = {}
        if dictionary is not None:
            if isinstance(dictionary, OrderedDict):
                self.__dict = dictionary.__dict.copy()
                self.__keys = dictionary.__keys[:]
            else:
                self.__dict = dict(dictionary).copy()
                self.__keys = sorted(self.__dict.keys())


    def update(self, dictionary=None, **kwargs):
        """Updates this dictionary with another dictionary and/or with
        keyword key=value pairs


        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5))
        >>> d.update(dict(a=4, z=-4))
        >>> d.items()
        [('a', 4), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('z', -4)]
        >>> del d["a"]
        >>> del d["i"]
        >>> d.update({'g': 9}, a=1, z=3)
        >>> d.items()
        [('a', 1), ('g', 9), ('n', 3), ('s', 1), ('t', 5), ('z', 3)]
        >>> e = OrderedDict(dict(p=4, q=5))
        >>> del d["a"]
        >>> del d["n"]
        >>> e.update(d)
        >>> e.items()
        [('g', 9), ('p', 4), ('q', 5), ('s', 1), ('t', 5), ('z', 3)]
        """
        if dictionary is None:
            pass
        elif isinstance(dictionary, OrderedDict):
            self.__dict.update(dictionary.__dict)
        elif (isinstance(dictionary, dict) or 
              not hasattr(dictionary, "items")):
            self.__dict.update(dictionary)
        else:
            for key, value in dictionary.items():
                self.__dict[key] = value
        if kwargs:
            self.__dict.update(kwargs)
        self.__keys = sorted(self.__dict.keys())


    @classmethod
    def fromkeys(cls, iterable, value=None):
        """A class method that returns an OrderedDict whose keys are
        from the iterable and each of whose values is value

        >>> d = OrderedDict()
        >>> e = d.fromkeys("KYLIE", 21)
        >>> e.items()
        [('E', 21), ('I', 21), ('K', 21), ('L', 21), ('Y', 21)]
        >>> e = OrderedDict.fromkeys("KYLIE", 21)
        >>> e.items()
        [('E', 21), ('I', 21), ('K', 21), ('L', 21), ('Y', 21)]
        """
        dictionary = cls()
        for key in iterable:
            dictionary[key] = value
        return dictionary


    def getAt(self, index):
        """Returns the index-th item's value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.getAt(0)
        2
        >>> d.getAt(5)
        6
        >>> d.getAt(2)
        3
        >>> d.getAt(19)
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        """
        return self.__dict[self.__keys[index]]


    def setAt(self, index, value):
        """Sets the index-th item's value to the given value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.getAt(5)
        6
        >>> d.setAt(5, 99)
        >>> d.getAt(5)
        99
        >>> d.setAt(19, 42)
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        """
        self.__dict[self.__keys[index]] = value


    def copy(self):
        """Returns a shallow copy of this OrderedDict

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> e = d.copy()
        >>> e.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        dictionary = OrderedDict()
        dictionary.__keys = self.__keys[:]
        dictionary.__dict = self.__dict.copy()
        return dictionary


    def clear(self):
        """Removes every item from this OrderedDict
        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> d.clear()
        >>> len(d)
        0
        >>> d["m"] = 3
        >>> d["a"] = 5
        >>> d["z"] = 7
        >>> d["e"] = 9
        >>> d.keys()
        ['a', 'e', 'm', 'z']
        """
        self.__keys = []
        self.__dict = {}


    def get(self, key, value=None):
        """Returns the value associated with key or value if key isn't
        in the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.get("X", 21)
        21
        >>> d.get("i")
        4
        """
        return self.__dict.get(key, value)


    def setdefault(self, key, value):
        """If key is in the dictionary, returns its value;
        otherwise adds the key with the given value which is also
        returned

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.setdefault("n", 99)
        3
        >>> d.values()
        [2, 4, 3, 1, 5, 6]
        >>> d.setdefault("r", -20)
        -20
        >>> d.items()[2:]
        [('n', 3), ('r', -20), ('s', 1), ('t', 5), ('y', 6)]
        >>> d.setdefault("@", -11)
        -11
        >>> d.setdefault("z", 99)
        99
        >>> d.setdefault("m", 50)
        50
        >>> d.keys()
        ['@', 'a', 'i', 'm', 'n', 'r', 's', 't', 'y', 'z']
        """
        if key not in self.__dict:
            bisect.insort_left(self.__keys, key)
        return self.__dict.setdefault(key, value)


    def pop(self, key, value=None):
        """If key is in the dictionary, returns its value and removes it
        from the dictionary; otherwise returns the given value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.pop("n")
        3
        >>> "n" in d
        False
        >>> d.pop("q", 41)
        41
        >>> d.keys()
        ['a', 'i', 's', 't', 'y']
        >>> d.pop("a")
        2
        >>> d.pop("t")
        5
        >>> d.keys()
        ['i', 's', 'y']
        """
        if key not in self.__dict:
            return value
        i = bisect.bisect_left(self.__keys, key)
        del self.__keys[i]
        return self.__dict.pop(key, value)


    def popitem(self):
        """Returns and removes an arbitrary item from the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> item = d.popitem()
        >>> item = d.popitem()
        >>> item = d.popitem()
        >>> len(d)
        3
        """
        item = self.__dict.popitem()
        i = bisect.bisect_left(self.__keys, item[0])
        del self.__keys[i]
        return item


    def keys(self):
        """Returns the dictionary's keys in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.keys()
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return self.__keys[:]


    def values(self):
        """Returns the dictionary's values in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.values()
        [2, 4, 3, 1, 5, 6]
        """
        return [self.__dict[key] for key in self.__keys]


    def items(self):
        """Returns the dictionary's items in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        return [(key, self.__dict[key]) for key in self.__keys]


    def __iter__(self):
        """Returns an iterator over the dictionary's keys

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d)
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return iter(self.__keys)


    def iterkeys(self):
        """Returns an iterator over the dictionary's keys

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d)
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return iter(self.__keys)


    def itervalues(self):
        """Returns an iterator over the dictionary's values in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d.itervalues())
        [2, 4, 3, 1, 5, 6]
        """
        for key in self.__keys:
            yield self.__dict[key]


    def iteritems(self):
        """Returns an iterator over the dictionary's values in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d.iteritems())
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        for key in self.__keys:
            yield key, self.__dict[key]


    def has_key(self, key):
        """Returns True if key is in the dictionary; otherwise returns
        False. Use in instead.

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.has_key("a")
        True
        >>> d.has_key("x")
        False
        """
        return key in self.__dict


    def __contains__(self, key):
        """Returns True if key is in the dictionary; otherwise returns
        False

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> "a" in d
        True
        >>> "x" in d
        False
        """
        return key in self.__dict


    def __len__(self):
        """Returns the number of items in the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> del d["n"]
        >>> del d["y"]
        >>> len(d)
        4
        >>> d.clear()
        >>> len(d)
        0
        """
        return len(self.__dict)


    def __delitem__(self, key):
        """Deletes the item with the given key from the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.keys()
        ['a', 'i', 'n', 's', 't', 'y']
        >>> del d["s"]
        >>> d.keys()
        ['a', 'i', 'n', 't', 'y']
        >>> del d["y"]
        >>> d.keys()
        ['a', 'i', 'n', 't']
        >>> del d["a"]
        >>> d.keys()
        ['i', 'n', 't']
        >>> d = OrderedDict(dict(a=1, b=2, z=3))
        >>> d.keys()
        ['a', 'b', 'z']
        >>> del d["c"]
        Traceback (most recent call last):
        ...
        KeyError: 'c'
        >>> d.keys()
        ['a', 'b', 'z']
        """
        del self.__dict[key]
        i = bisect.bisect_left(self.__keys, key)
        del self.__keys[i]


    def __getitem__(self, key):
        """Returns the value of the item with the given key

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d["i"]
        4
        >>> d["y"]
        6
        >>> d["z"]
        Traceback (most recent call last):
        ...
        KeyError: 'z'
        """
        return self.__dict[key]


    def __setitem__(self, key, value):
        """If key is in the dictionary, sets its value to value;
        otherwise adds the key to the dictionary with the given value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d["t"] = -17
        >>> d["z"] = 43
        >>> d["@"] = -11
        >>> d["m"] = 22
        >>> d["r"] = 5
        >>> d.keys()
        ['@', 'a', 'i', 'm', 'n', 'r', 's', 't', 'y', 'z']
        """
        if key not in self.__dict:
            bisect.insort_left(self.__keys, key)
        self.__dict[key] = value


    def __repr__(self):
        """Returns an eval()-able string representation of the
        dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5))
        >>> repr(d)
        "OrderedDict({'a': 2, 'i': 4, 'n': 3, 's': 1, 't': 5})"
        >>> d = OrderedDict({2: 'a', 3: 'm', 1: 'x'})
        >>> repr(d)
        "OrderedDict({1: 'x', 2: 'a', 3: 'm'})"

        Alternative implementation using a list comprehension:

        return "OrderedDict({{{0}}})".format(", ".join(
               ["{0!r}: {1!r}".format((key, self.__dict[key])) \
                for key in self.__keys]))
        """
        pieces = []
        for key in self.__keys:
            pieces.append("{0!r}: {1!r}".format(key, self.__dict[key]))
        return "OrderedDict({{{0}}})".format(", ".join(pieces))

""" Enregistreur de données dans un fichier """
class dicovar(dict):
    def __init__(self, nf):
        self.nf = nf
        try:
            f=open(nf, 'r')
            dict.__init__(self, eval(f.readline().rstrip('\r\n')))
            f.close()
        except:
            dict.__init__(self, {})
 
    def enregistre(self):
        f=open(self.nf, 'w')
        f.write(repr(self) + os.linesep)
        f.close()

""" permet de dimensionner automatiquement les colonnes d'un tableau reportsLab"""
def colonneDimAuto(t=None,l=5.8):
    """ 42 CAR POUR 200 DONC 200/42"""
    try:
        if t:return map(lambda x:x*l, map(lambda x:max([len(str(y)) for y in x]), zip(*t)))
    except:return [5]
    
def grouperListe(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def partagerListe(t=None,n=2):
    z=[]
    if n:
        if t and not len(t)%n:
            a=int(len(t)/n)
            for i in list(range(1,len(t)+1)):
                if not i%a:
                    z.append(t[i-a:i])
        else:print (u't est vide ou le reste de la division ne donne pas zéro')
    else:print (u'n est égale à zéro')                      
    return z


def dateAnglais(x=None):
    if x:
        x=str(x)[:10]
        p=tuple([(int(i)) for i in x.split('/')])
        return datetime.date(p[2],p[1],p[0])


def dateFrenchEnglish(x=None):
    if x:
        try:
            x = str(x)
            x = x[3:5]+'-'+ x[:2]+'-'+ x[6:]
        except:
            pass
    else:x=""
    return x


def dateFrancaisAnglais(x=None):
    if x:
        try:
            x = str(x)
            x = x[3:5]+'/'+ x[:2]+'/'+ x[6:]
        except:
            pass
    else:x=""
    return x


def dateAnglaisFrancais(x=None):
    if x:
        try:
            x=str(x)
            x=x[:10]
            x=x[8:]+'/'+x[5:7]+'/'+x[:4]
        except:pass
    else:x=""
    return x


""" mettre les premières lettres d'un groupe de mots en majuscule """
def Title(c=None):
    c=unicode(c)
    q=c.split()
    if q:
        popo = QLineEdit()
        popo.setText(reduce(lambda x,y:x+' '+y,map(lambda x: x[0].upper()+x[1:].lower(),[i for i in q])))
        return popo.text().toUtf8()
    return c 
 
def AfficheEntier(n, sep = "."):
    plusmoins=''
    s=str(n)
    if s[0]=='-':
        plusmoins='-'
        s=s[1:]
    l=len(s)

    d=int(l/3)
    for i in range(1,d+1):
        s=s[:l-3*i]+sep+s[l-3*i:]
    if plusmoins:s='-'+s
    return s

def AfficheEntier1(n, sep = "'"):
    """Affiche un nombre entier n, en utilisant sep comme séparateur des milliers"""
    s = str(n)
    l = len(s)
    nc = 0
    res = ""
    for i in range(l-1, -1, -1):
        res = s[i] + res
        nc += 1
        if nc == 3:
            res = sep + res
            nc = 0
    if res.startswith(sep):
        res = res[1:]
    if n < 0 and res[1] == sep:
        res = list(res)
        del res[1]
        res = "".join(res)
    return res


def simplify(text, space=" \t\r\n\f", delete=""):
    """Returns the text with multiple spaces reduced to single spaces
    The space parameter is a string of characters each of which is
    considered to be a space.
    Any characters in delete are excluded from the resultant string.
    >>> simplify(" this    and\\n that\\t too")
    'this and that too'
    >>> simplify("  Washington   D.C.\\n")
    'Washington D.C.'
    >>> simplify("  Washington   D.C.\\n", delete=",;:.")
    'Washington DC'
    >>> simplify(" disemvoweled ", delete="aeiou")
    'dsmvwld'
    """
    result = []
    word = ""
    for char in text:
        if char in delete:
            continue
        elif char in space:
            if word:
                result.append(word)
                word = ""
        else:
            word += char
    if word:
        result.append(word)
    return " ".join(result)


def nombre(text):
    try:
        text = simplify(str(text), delete=' ')
        if '.' in text:return float(text)
        else:return int(text)
    except:return 0


def millier(text):
    try:
        text = simplify(str(text), delete=' ')
        return AfficheEntier(text, ' ').strip()
    except:return text

"""
class Intervallometre(threading.Thread):
    def __init__(self, duree, fonction, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.duree = duree
        self.fonction = fonction
        self.args = args
        self.kwargs = kwargs
        self.encore = True  # pour permettre l'arret a la demande
 
    def run(self):
        while self.encore:
            self.timer = threading.Timer(self.duree, self.fonction, self.args, self.kwargs)
            self.timer.setDaemon(True)
            self.timer.start()
            self.timer.join()
 
    def stop(self):
        self.encore = False  # pour empecher un nouveau lancement de Timer et terminer le thread
        if self.timer.isAlive():
            self.timer.cancel()  # pour terminer une eventuelle attente en cours de Timer


# -*- coding: cp1252 -*-
import threading
import time
class MyTimer:
    def __init__(self, tempo, target, args= [], kwargs={}):
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._tempo = tempo
        
    def _run(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()
        self._target(*self._args, **self._kwargs)
        
    def start(self):
        self._timer = threading.Timer(self._tempo, self._run)
        self._timer.start()
    
    def stop(self):
        self._timer.cancel()
"""            

def aplatliste(L):
    R = []
    for elem in L:
        if isinstance(elem, (list, tuple)):
            R.extend(aplatliste(elem))
        else:
            R.append(elem)
    return R

def extraireDoublon(t=None):
    if t:
        x=[]
        for i in t:
            if i not in x:
                x.append(i)
        return x
    print ('La liste est vide')       

def compterOccurence2(t=None):
    if t:
        x=y=[]
        for i in t:
            if i not in x:
                x.append(i)
                y.append((u'{0}'.format(i), t.count(i)))
                print (u'le nombre de {0} est {1}'.format(i, t.count(i)))
        #y.sort(reverse = True)        
        return y
    print('la liste est vide')

def qsort(L):
    if len(L) <= 1: return L
    return qsort( [ lt for lt in L[1:] if lt < L[0] ] )  +  [ L[0] ]  +  qsort( [ ge for ge in L[1:] if ge >= L[0] ] )

def formate(x, nbc=-15, decod="utf-8", encod=None):
    """transforme en chaine un objet imprimable avec le bon formatage des flottants et le bon encodage des chaines
  - nbc: nombre de chiffres pour les flottants:
    - Si nbc<0: abs(nbc) chiffres significatifs.
    - Si nbc>=0: nbc chiffres après la virgule.
  - decod: encodage des chaines non-unicode (pour les chaines du code source: mettre l'encodage du code source)
  - encod: encodage voulu pour la chaine de sortie (pour l'affichage: trouve encodage de la console)
"""
 
    if encod==None:
        encod = sys.stdout.encoding
        if encod==None:
            encod = 'utf-8'  # cas particulier de la console d'eclipse
 
    if isinstance(x,int) or isinstance(x,long):
        return "%d" % (x)
 
    elif isinstance(x,float):
        f = "%d" % (abs(nbc))
        if nbc<0:
            f = "%." + f + "g"
        else:
            f = "%." + f + "f"
        return f % (x)
 
    elif isinstance(x,complex):
        L = "("
        y = x.real
        if isinstance(y,float) and float(int(y))==y:
            y=int(y)
        L += formate(y,nbc,encod,decod)
        y = x.imag
        if isinstance(y,float) and float(int(y))==y:
            y=int(y)
        if y>=0:
            L += "+"
        L += formate(y,nbc,encod,decod) + "j)"
        return L
 
    elif isinstance(x,str):
        return '"%s"' % (x.decode(decod).encode(encod,'replace'))
         
    elif isinstance(x,unicode):
        return '"%s"' % (x.encode(encod,'replace'))
        
 
    elif isinstance(x,list):
        L = "["
        if x!=[]:
            for elem in x:
                L += "%s, " % formate(elem,nbc,decod,encod)
            L=L[:-2]
        L += "]"
        return L
 
    elif isinstance(x,tuple):
        L = "("
        if x!=():
            for elem in x:
                L += "%s, " % formate(elem,nbc,decod,encod)
            L = L[:-2]
        L += ")"
        return L
 
    elif isinstance(x,dict):
        L = "{"
        if x!={}:
            for k, v in x.iteritems():
                L += '%s:%s, ' % (formate(k,nbc,decod,encod), formate(v,nbc,decod,encod))
            L = L[:-2]
        L += "}"
        return L
 
    else:
        return "%s" % (x)
    
    
        
def datePaques(an):
    """Calcule la date de Pâques d'une année donnée an (=nombre entier)"""
    a=an//100
    b=an%100
    c=(3*(a+25))//4
    d=(3*(a+25))%4
    e=(8*(a+11))//25
    f=(5*a+b)%19
    g=(19*f+c-e)%30
    h=(f+11*g)//319
    j=(60*(5-d)+b)//4
    k=(60*(5-d)+b)%4
    m=(2*j-k-g+h)%7
    n=(g-h+m+114)//31
    p=(g-h+m+114)%31
    jour=p+1
    mois=n
    return [jour, mois, an]

def iif(condition, valeurOui='', valeurNon=''):
    if condition:return valeurOui
    else:return valeurNon


def chiffreLettre(nombre=0):
    if nombre>-1:
        if (0<len(str(nombre))<=12):
            unite = {0:"zéro", 1:"un", 2:"deux", 3:"trois", 4:"quatre", 5:"cinq", 6:"six", 7:"sept", 8:"huit", 9:"neuf"}
            dizaine = {0:"zéro", 1:"un", 2:"deux", 3:"trois", 4:"quatre", 5:"cinq", 6:"six", 7:"sept", 8:"huit", 9:"neuf",
                       10:"dix", 11:"onze", 12:"douze", 13:"treize", 14:"quatorze", 15:"quinze", 16:"seize", 17:"dix sept",
                       18:"dix huit", 19:"dix neuf", 20:"vingt", 21:"vingt et un", 22:"vingt deux", 23:"vingt trois",
                       24:"vingt quatre", 25:"vingt cinq", 26:"vingt six", 27:"vingt sept", 28:"vingt huit", 29:"vingt neuf",
                       30:"trente", 31:"trente et un", 32:"trente deux", 33:"trente trois", 34:"trente quatre", 35:"trente cinq",
                       36:"trente six", 37:"trente sept", 38:"trente huit", 39:"trente neuf", 40:"quarante", 41:"quarante et un",
                       42:"quarante deux", 43:"quarante trois", 44:"quarante quatre", 45:"quarante cinq", 46:"quarante six",
                       47:"quarante sept", 48:"quarante huit", 49:"quarante neuf", 50:"cinquante", 51:"cinquante et un",
                       52:"cinquante deux", 53:"cinquante trois", 54:"cinquante quatre", 55:"cinquante cinq", 56:"cinquante six",
                       57:"cinquante sept", 58:"cinquante huit", 59:"cinquante neuf", 60:"soixante", 61:"soixante et un",
                       62:"soixante deux", 63:"soixante trois", 64:"soixante quatre", 65:"soixante cinq", 66:"soixante six",
                       67:"soixante sept", 68:"soixante huit", 69:"soixante neuf", 70:"soixante dix", 71:"soixante onze",
                       72:"soixante douze", 73:"soixante treize", 74:"soixante quatorze", 75:"soixante quinze", 76:"soixante seize",
                       77:"soixante dix sept", 78:"soixante dix huit", 79:"soixante dix neuf", 80:"quatre vingt", 81:"quatre vingt et un",
                       82:"quatre vingt deux", 83:"quatre vingt trois", 84:"quatre vingt quatre", 85:"quatre vingt cinq", 86:"quatre vingt six",
                       87:"quatre vingt sept", 88:"quatre vingt huit", 89:"quatre vingt neuf", 90:"quatre vingt dix",
                       91:"quatre vingt onze", 92:"quatre vingt douze", 93:"quatre vingt treize", 94:"quatre vingt quatorze",
                       95:"quatre vingt quinze", 96:"quatre vingt seize", 97:"quatre vingt dix sept", 98:"quatre vingt dix huit",
                       99:"quatre vingt dix neuf"}
            lettre=chiffre=donnee=""
            nombre=str(nombre)
            while len(nombre)>0:
                if (len(nombre)==12 or len(nombre)==9):
                    donnee = nombre[:3]
                    chiffre = unite[int(donnee[0])]
                    lettre += iif(chiffre not in ('zéro', 'un'), chiffre) + iif(chiffre != "zéro", ' cent ')
                    chiffre = dizaine[int(donnee[1:])]
                    lettre += iif(len(nombre)==12, iif(chiffre != "zéro", chiffre) + iif(chiffre != "zéro", ' millards ', 'milliards '),\
                        iif(chiffre != "zéro", chiffre) + iif(chiffre != "zéro", ' millions '))
                    nombre = nombre[3:]

                if (len(nombre)==11 or len(nombre)==8):
                    donnee = nombre[:2]
                    chiffre = dizaine[int(donnee)]
                    lettre += iif(len(nombre)==12, iif(chiffre != "zéro", chiffre) + iif(chiffre != "zéro", ' milliards '), iif(chiffre != "zéro", chiffre) + iif(chiffre != "zéro", ' millions '))
                    nombre = nombre[2:]
                                
                if len(nombre)==10:
                    donnee = nombre[0]
                    chiffre = unite[int(donnee)]
                    lettre += iif(chiffre != "zéro", chiffre) + iif(chiffre != "zéro",' millards ') 
                    nombre = nombre[3:]                  
            
                if len(nombre)==7:
                    donnee = nombre[0]
                    chiffre = unite[int(donnee)]
                    lettre += iif(chiffre != "zéro", chiffre) + iif(chiffre != "zéro", iif(chiffre != 'un', ' millions ', ' million '))         
                    if nombre=='1000000':
                        nombre=""
                        return lettre
                    nombre = nombre[1:]
            
                if len(nombre)==6:
                    donnee = nombre[:3]
                    chiffre = unite[int(donnee[0])]
                    lettre += iif(chiffre not in ("zéro", "un"), chiffre) + iif(chiffre != "zéro", ' cent ','')
                    chiffre = dizaine[int(donnee[1:])]
                    lettre += iif(chiffre != "zéro", iif(chiffre != "un", chiffre)) + iif(chiffre != "zéro", ' mille ', 'mille ') 
                    nombre = nombre[3:]        
                
                if len(nombre)==5:
                    donnee = nombre[:2]
                    chiffre = dizaine[int(donnee)]
                    lettre += iif(chiffre != 'zéro', chiffre) + iif(chiffre != "zéro", ' mille ')
                    nombre = nombre[2:]
                
                if len(nombre)==4:
                    donnee = nombre[0]
                    chiffre = unite[int(donnee)]
                    lettre += iif(chiffre != "un", chiffre) + iif(chiffre != "zéro", ' mille ') 
                    nombre = nombre[1:]
            
                if len(nombre)==3:
                    chiffre = unite[int(nombre[0])]
                    lettre += iif(chiffre not in ("zéro", "un"), chiffre + ' ')+ iif(chiffre != "zéro", "cent ")
                    chiffre = dizaine[int(nombre[1:])]
                    lettre += iif(chiffre != "zéro", chiffre)
                    nombre = ""
                   
                if len(nombre)==2:
                    lettre = dizaine[int(nombre)]
                    nombre = ""

                if len(nombre)==1:
                    lettre = unite[int(nombre)]
                    nombre = ""
            return lettre
    else:return 'moins ' + chiffreLettre(abs(nombre))#'le nombre est négatif ou est supérieur au milliard'

        

def rang(t=None):
    """ t[(valeur, index)] """
    flag=False
    
    g={}
    if t:
        save=filter(lambda x:x[0] in (None, 'nc'), t[:])
        if save:
            flag=True
            save=set(save)
            t=set(t)
            t=t-save
            t=list(t)
            save=list(save)
            sav={}
            for i in save:sav[i[1]]=('nc', i[1], 'nc')
        t.sort(reverse=True)
        v=[]
        i=[]
        r=[]
        f=[]
        tampon=[]
        """ dictionnaire g = {cle :(valeur, cle, rang)} """
        g={} 
        
        for m in t:
            if m[0] in v:
                v.append(m[0])
                i.append(m[1])
                r.append(r[v.index(m[0])])
                f.append((m[0],m[1],r[v.index(m[0])]))
                """ On donne le rang exéco à l'élément doublon """
                #g[m[1]]=((m[0],m[1],str(r[v.index(m[0])])+u' ème ex.'))
                g[m[1]]=((m[0],m[1],str(r[v.index(m[0])])+iif(r[v.index(m[0])]==1,u'e ex',u'ème ex')))
                
                """ On donne le rang exéco au premier élément trouvé """
                g[tampon[1]]=((tampon[0],tampon[1],str(r[v.index(tampon[0])])+iif(r[v.index(m[0])]==1,u'e ex',u'ème ex')))
            else:
                v.append(m[0])
                i.append(m[1])
                r.append(t.index(m)+1)
                f.append((m[0],m[1],t.index(m)+1))
                g[m[1]]=((m[0],m[1],str(r[v.index(m[0])])+ iif(r[v.index(m[0])]!=1, u'ème','e')))
                """ on sauvegarde les premières occurrences dans tampon """
                tampon = m[:]
        if flag:g.update(sav)
        return g

def ranganc(t=None):
    """ t[(valeur, index)] """
    g={}
    if t:
        t.sort(reverse=True)
        v=[]
        i=[]
        r=[]
        f=[]
        tampon=[]
        """ dictionnaire g = {cle :(valeur, cle, rang)} """
        g={} 
        
        for m in t:
            if m[0] in v:
                v.append(m[0])
                i.append(m[1])
                r.append(r[v.index(m[0])])
                f.append((m[0],m[1],r[v.index(m[0])]))
                """ On donne le rang exéco à l'élément doublon """
                #g[m[1]]=((m[0],m[1],str(r[v.index(m[0])])+u' ème ex.'))
                g[m[1]]=((m[0],m[1],str(r[v.index(m[0])])+iif(r[v.index(m[0])]==1,u'e ex',u'e ex')))
                
                """ On donne le rang exéco au premier élément trouvé """
                g[tampon[1]]=((tampon[0],tampon[1],str(r[v.index(tampon[0])])+iif(r[v.index(m[0])]==1,u'e ex',u'e ex')))
            else:
                v.append(m[0])
                i.append(m[1])
                r.append(t.index(m)+1)
                f.append((m[0],m[1],t.index(m)+1))
                g[m[1]]=((m[0],m[1],str(r[v.index(m[0])])+ iif(r[v.index(m[0])]!=1, u'e','e')))
                """ on sauvegarde les premières occurrences dans tampon """
                tampon = m[:]
        return g
    
""" Objet des connection et command """
class Connection():
    def __init__(self, source="source"):
        self.source = source
        adodbapi.adodbapi.verbose = False # adds details to the sample printout
        # connection string templates from http://www.connectionstrings.com
        # Switch test providers by changing the "if True" below
        # connection string for an Access data table:
        if True:
            constr = '%s' % (source)
            #-----------------
            #tell the server  we are not planning to update...
            #adodbapi.adodbapi.defaultIsolationLevel = adodbapi.adodbapi.adXactCommitRetaining
            #and we want a local cursor (so that we will have an accurate rowcount)
            #adodbapi.adodbapi.defaultCursorLocation = adodbapi.adodbapi.adCmdText
            #create the connection
            self.cnn = adodbapi.connect(constr)
            #make a cursor on the connection
            self.cmd = self.cnn.cursor()
            #renvoie la connection = cnn et la command = cmd
            print ('Connection OK')
            #return self.cnn, self.cmd
        else:
            #return None, None
            print ("La connection a échoué")
    
    
    """ Lire les infoos des Bases de données  """
    def lireDonnee(self, sqlText=None):
        """ Execution de la requete """
        if sqlText==None:
            return []
        self.cmd.execute(unicode(sqlText, 'utf8'))
        """ la variable m recoit le recordset """
        m = self.cmd.fetchall()
        if len(m)>0:
            """ m est un ensemble de tuples
            rendre ces tuples en chaine de caracteres normale """
            p=[]
            for i in m:
                q=[]
                for j in i:
                    """ les données sont converties en chaîne de caractères """
                    if 'DateTime' in str(type(j)).split('.'):
                        q.append(j.date)
                    else:
                        q.append(j)
                p.append(q)
            return p
        else:
            return []    
    
class OrderedDict(object):
    
    """A dictionary that is ordered by key
    
    Initializing with a dictionary is expensive because all the
    dictionary's keys must be sorted. This is also true of the update()
    method.
    """

    def __init__(self, dictionary=None):
        """Initializes with a shallow copy of the given dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        >>> OrderedDict()
        OrderedDict({})
        >>> e = OrderedDict(d)
        >>> e.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        self.__keys = []
        self.__dict = {}
        if dictionary is not None:
            if isinstance(dictionary, OrderedDict):
                self.__dict = dictionary.__dict.copy()
                self.__keys = dictionary.__keys[:]
            else:
                self.__dict = dict(dictionary).copy()
                self.__keys = sorted(self.__dict.keys())


    def update(self, dictionary=None, **kwargs):
        """Updates this dictionary with another dictionary and/or with
        keyword key=value pairs


        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5))
        >>> d.update(dict(a=4, z=-4))
        >>> d.items()
        [('a', 4), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('z', -4)]
        >>> del d["a"]
        >>> del d["i"]
        >>> d.update({'g': 9}, a=1, z=3)
        >>> d.items()
        [('a', 1), ('g', 9), ('n', 3), ('s', 1), ('t', 5), ('z', 3)]
        >>> e = OrderedDict(dict(p=4, q=5))
        >>> del d["a"]
        >>> del d["n"]
        >>> e.update(d)
        >>> e.items()
        [('g', 9), ('p', 4), ('q', 5), ('s', 1), ('t', 5), ('z', 3)]
        """
        if dictionary is None:
            pass
        elif isinstance(dictionary, OrderedDict):
            self.__dict.update(dictionary.__dict)
        elif (isinstance(dictionary, dict) or 
              not hasattr(dictionary, "items")):
            self.__dict.update(dictionary)
        else:
            for key, value in dictionary.items():
                self.__dict[key] = value
        if kwargs:
            self.__dict.update(kwargs)
        self.__keys = sorted(self.__dict.keys())


    @classmethod
    def fromkeys(cls, iterable, value=None):
        """A class method that returns an OrderedDict whose keys are
        from the iterable and each of whose values is value

        >>> d = OrderedDict()
        >>> e = d.fromkeys("KYLIE", 21)
        >>> e.items()
        [('E', 21), ('I', 21), ('K', 21), ('L', 21), ('Y', 21)]
        >>> e = OrderedDict.fromkeys("KYLIE", 21)
        >>> e.items()
        [('E', 21), ('I', 21), ('K', 21), ('L', 21), ('Y', 21)]
        """
        dictionary = cls()
        for key in iterable:
            dictionary[key] = value
        return dictionary


    def getAt(self, index):
        """Returns the index-th item's value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.getAt(0)
        2
        >>> d.getAt(5)
        6
        >>> d.getAt(2)
        3
        >>> d.getAt(19)
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        """
        return self.__dict[self.__keys[index]]


    def setAt(self, index, value):
        """Sets the index-th item's value to the given value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.getAt(5)
        6
        >>> d.setAt(5, 99)
        >>> d.getAt(5)
        99
        >>> d.setAt(19, 42)
        Traceback (most recent call last):
        ...
        IndexError: list index out of range
        """
        self.__dict[self.__keys[index]] = value


    def copy(self):
        """Returns a shallow copy of this OrderedDict

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> e = d.copy()
        >>> e.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        dictionary = OrderedDict()
        dictionary.__keys = self.__keys[:]
        dictionary.__dict = self.__dict.copy()
        return dictionary


    def clear(self):
        """Removes every item from this OrderedDict
        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> d.clear()
        >>> len(d)
        0
        >>> d["m"] = 3
        >>> d["a"] = 5
        >>> d["z"] = 7
        >>> d["e"] = 9
        >>> d.keys()
        ['a', 'e', 'm', 'z']
        """
        self.__keys = []
        self.__dict = {}


    def get(self, key, value=None):
        """Returns the value associated with key or value if key isn't
        in the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.get("X", 21)
        21
        >>> d.get("i")
        4
        """
        return self.__dict.get(key, value)


    def setdefault(self, key, value):
        """If key is in the dictionary, returns its value;
        otherwise adds the key with the given value which is also
        returned

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.setdefault("n", 99)
        3
        >>> d.values()
        [2, 4, 3, 1, 5, 6]
        >>> d.setdefault("r", -20)
        -20
        >>> d.items()[2:]
        [('n', 3), ('r', -20), ('s', 1), ('t', 5), ('y', 6)]
        >>> d.setdefault("@", -11)
        -11
        >>> d.setdefault("z", 99)
        99
        >>> d.setdefault("m", 50)
        50
        >>> d.keys()
        ['@', 'a', 'i', 'm', 'n', 'r', 's', 't', 'y', 'z']
        """
        if key not in self.__dict:
            bisect.insort_left(self.__keys, key)
        return self.__dict.setdefault(key, value)


    def pop(self, key, value=None):
        """If key is in the dictionary, returns its value and removes it
        from the dictionary; otherwise returns the given value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.pop("n")
        3
        >>> "n" in d
        False
        >>> d.pop("q", 41)
        41
        >>> d.keys()
        ['a', 'i', 's', 't', 'y']
        >>> d.pop("a")
        2
        >>> d.pop("t")
        5
        >>> d.keys()
        ['i', 's', 'y']
        """
        if key not in self.__dict:
            return value
        i = bisect.bisect_left(self.__keys, key)
        del self.__keys[i]
        return self.__dict.pop(key, value)


    def popitem(self):
        """Returns and removes an arbitrary item from the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> item = d.popitem()
        >>> item = d.popitem()
        >>> item = d.popitem()
        >>> len(d)
        3
        """
        item = self.__dict.popitem()
        i = bisect.bisect_left(self.__keys, item[0])
        del self.__keys[i]
        return item


    def keys(self):
        """Returns the dictionary's keys in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.keys()
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return self.__keys[:]


    def values(self):
        """Returns the dictionary's values in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.values()
        [2, 4, 3, 1, 5, 6]
        """
        return [self.__dict[key] for key in self.__keys]


    def items(self):
        """Returns the dictionary's items in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.items()
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        return [(key, self.__dict[key]) for key in self.__keys]


    def __iter__(self):
        """Returns an iterator over the dictionary's keys

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d)
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return iter(self.__keys)


    def iterkeys(self):
        """Returns an iterator over the dictionary's keys

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d)
        ['a', 'i', 'n', 's', 't', 'y']
        """
        return iter(self.__keys)


    def itervalues(self):
        """Returns an iterator over the dictionary's values in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d.itervalues())
        [2, 4, 3, 1, 5, 6]
        """
        for key in self.__keys:
            yield self.__dict[key]


    def iteritems(self):
        """Returns an iterator over the dictionary's values in key order

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> list(d.iteritems())
        [('a', 2), ('i', 4), ('n', 3), ('s', 1), ('t', 5), ('y', 6)]
        """
        for key in self.__keys:
            yield key, self.__dict[key]


    def has_key(self, key):
        """Returns True if key is in the dictionary; otherwise returns
        False. Use in instead.

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.has_key("a")
        True
        >>> d.has_key("x")
        False
        """
        return key in self.__dict


    def __contains__(self, key):
        """Returns True if key is in the dictionary; otherwise returns
        False

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> "a" in d
        True
        >>> "x" in d
        False
        """
        return key in self.__dict


    def __len__(self):
        """Returns the number of items in the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> len(d)
        6
        >>> del d["n"]
        >>> del d["y"]
        >>> len(d)
        4
        >>> d.clear()
        >>> len(d)
        0
        """
        return len(self.__dict)


    def __delitem__(self, key):
        """Deletes the item with the given key from the dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d.keys()
        ['a', 'i', 'n', 's', 't', 'y']
        >>> del d["s"]
        >>> d.keys()
        ['a', 'i', 'n', 't', 'y']
        >>> del d["y"]
        >>> d.keys()
        ['a', 'i', 'n', 't']
        >>> del d["a"]
        >>> d.keys()
        ['i', 'n', 't']
        >>> d = OrderedDict(dict(a=1, b=2, z=3))
        >>> d.keys()
        ['a', 'b', 'z']
        >>> del d["c"]
        Traceback (most recent call last):
        ...
        KeyError: 'c'
        >>> d.keys()
        ['a', 'b', 'z']
        """
        del self.__dict[key]
        i = bisect.bisect_left(self.__keys, key)
        del self.__keys[i]


    def __getitem__(self, key):
        """Returns the value of the item with the given key

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d["i"]
        4
        >>> d["y"]
        6
        >>> d["z"]
        Traceback (most recent call last):
        ...
        KeyError: 'z'
        """
        return self.__dict[key]


    def __setitem__(self, key, value):
        """If key is in the dictionary, sets its value to value;
        otherwise adds the key to the dictionary with the given value

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5, y=6))
        >>> d["t"] = -17
        >>> d["z"] = 43
        >>> d["@"] = -11
        >>> d["m"] = 22
        >>> d["r"] = 5
        >>> d.keys()
        ['@', 'a', 'i', 'm', 'n', 'r', 's', 't', 'y', 'z']
        """
        if key not in self.__dict:
            bisect.insort_left(self.__keys, key)
        self.__dict[key] = value


    def __repr__(self):
        """Returns an eval()-able string representation of the
        dictionary

        >>> d = OrderedDict(dict(s=1, a=2, n=3, i=4, t=5))
        >>> repr(d)
        "OrderedDict({'a': 2, 'i': 4, 'n': 3, 's': 1, 't': 5})"
        >>> d = OrderedDict({2: 'a', 3: 'm', 1: 'x'})
        >>> repr(d)
        "OrderedDict({1: 'x', 2: 'a', 3: 'm'})"

        Alternative implementation using a list comprehension:

        return "OrderedDict({{{0}}})".format(", ".join(
               ["{0!r}: {1!r}".format((key, self.__dict[key])) \
                for key in self.__keys]))
        """
        pieces = []
        for key in self.__keys:
            pieces.append("{0!r}: {1!r}".format(key, self.__dict[key]))
        return "OrderedDict({{{0}}})".format(", ".join(pieces))