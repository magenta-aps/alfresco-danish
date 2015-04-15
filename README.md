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


If you are building an amp using the Alfreco Maven SDK and want to include these amps you might consider looking into creating a profile in your pom.xml for it (perhaps something along the lines of the 'unpack-deps'-profile listed below) and declare a dependency on the wanted amp (and a reference to the Magenta nexus repository).

```
	<profile>
            <id>unpack-deps</id>
            <build>
                <plugins>
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-dependency-plugin</artifactId>

                        <executions>
                            <execution>
                                <id>unpack-amps</id>
                                <phase>prepare-package</phase>
                                <goals>
                                    <goal>unpack-dependencies</goal>
                                </goals>
                                <configuration>
                                    <includeTypes>amp</includeTypes>
                                    <outputDirectory>${alfresco.client.war.folder}</outputDirectory>
                                </configuration>
                            </execution>
                        </executions>
                        <dependencies>
                            <dependency>
                                <groupId>org.alfresco.maven.plugin</groupId>
                                <artifactId>maven-amp-plugin</artifactId>
                                <version>3.0.2</version>
                            </dependency>

                        </dependencies>
                    </plugin>

                </plugins>
            </build>
        </profile>
```
Repository translations:
```
<dependency>
  <groupId>magenta-aps</groupId>
  <artifactId>alfresco_da_dk</artifactId>
  <version>5.0.0-SNAPSHOT</version>
  <type>amp</type>
</dependency>
```

Share translations:
```
<dependency>
  <groupId>magenta-aps</groupId>
  <artifactId>share_da_dk</artifactId>
  <version>5.0.0-SNAPSHOT</version>
  <type>amp</type>
</dependency>
```

Magenta Nexus Repository References:

```
    <repositories>
        <repository>
            <id>magenta-public</id>
            <url>http://nexus.magenta-aps.dk/nexus/content/repositories/Alfresco-RELEASES</url>
        </repository>
        <repository>
            <id>magenta-public-snapshots</id>
            <url>http://nexus.magenta-aps.dk/nexus/content/repositories/Alfresco-SNAPSHOTS</url>
            <snapshots>
                <enabled>true</enabled>
                <updatePolicy>daily</updatePolicy>
            </snapshots>
        </repository>
    </repositories>
```

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

  



