Danish Translation of Alfresco version 5
========================================

It is the intention to incorporate translations in this language pack from a Crowdin project: https://crowdin.com/project/alfresco

Please sign up there if you are interested in contributing with translations.

Packaged builds of this Github-repository can be found at Magenta's public maven repository. At the time of this writing only snapshot builds are avaliable at http://nexus.magenta-aps.dk/nexus/content/repositories/Alfresco-SNAPSHOTS/


Usage
-----
To use the pre-packaged amps directly in your alfresco installation, you can download alfresco_da_dk.amp and share_da_dk.amp, going through the urls listed below respectively.
 
* http://nexus.magenta-aps.dk/nexus/index.html#nexus-search;quick~share_da_dk
* http://nexus.magenta-aps.dk/nexus/index.html#nexus-search;quick~alfresco_da_dk

Place the alfresco_da_dk.amp in the 'amps'-folder of your alfresco installation and  share_da_dk.amp in 'amps_share' and run ./bin/apply_amps.sh


Building
--------

You should be able to build the language pack amps yourself following these steps: 

1. clone this repository
2. mvn clean install

After completing these steps you will find the amps files containing the translation in the target folders of each submodule and in your local maven repository.

Comparing / Integrating translations from Crowd-in / TinyMce-sources
----------

When you run the script ./refresh_crowdin_tinymce_workdir.sh it will create a folder name 'compare', and fetch the danish translations from Crowd-in and TinyMce directly from the sources. It will also try to create a directory-structure matching the layout of 'share' and 'repo'. This should facilitate the direct comparison of the directory structures, using your favorite tool supporting directory-comparison (like 'Meld','DeltaWalker' or 'Eclipse').

```
meld share/ compare/share/
```

and

```
meld repo/ compare/repo/
```

This should help you pick and choose translations, that you want to integrate into your language packs - as well as help you identify translations, that could be candidates for pushing 'upstream' to the sources (that is, Crowd-in and TinyMce).

  
FAQ
------

*	When using the suggested 'unpack-deps'-profile to apply the language pack when starting Share using maven ( mvn clean integration-test -Pamp-to-war -Punpack-deps') the danish translations of Aikau texts are not visible. Why is that?  

*	This is caused by the fact that currently, the tool used by maven when unpacking the language pack amp does not handle the "amp-to-war" file-mappings defined in the amp, the same way as ./bin/apply_amps.sh does. This means that the Aikua-translations are currently not placed in the right path when using maven to unpack the langauge pack - but they they are placed correctly (although duplicated) when deploying the amp using ./bin/apply_amps.sh from the alfresco installation directory.









