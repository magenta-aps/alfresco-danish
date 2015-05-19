Danish Translation of Alfresco version 5
========================================

It is the intention to incorporate translations in this language pack from a Crowdin project: https://crowdin.com/project/alfresco

Please sign up there if you are interested in contributing with translations.

Packaged builds of this Github-repository can be found at Magenta's public maven repository. At the time of this writing only snapshot builds are avaliable at http://nexus.magenta-aps.dk/nexus/content/repositories/Alfresco-SNAPSHOTS/


Open-E
--------

Please notice that translations, that property-file-wise are part of this language pack, but logically belongs to the project Magenta Open-E / OpenESDH (https://github.com/OpenESDH/openesdh-core), should be placed on the branch Magenta_OpenE_Specific_Translations.


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








