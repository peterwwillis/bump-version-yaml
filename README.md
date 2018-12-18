## What is it?

Python program to bump versions in YAML files.

## How does it work?

If you have a YAML file with version numbers in it, you create a second YAML file that maps the locations of the version numbers and declares how to bump the version number. Then you run the program and it'll parse the files and output the original YAML file with the version numbers bumped.

## Suggested Use

Say you have this kubernetes file:
```yaml
advisorUi: 
  replicaCount: 3
  image:
    dockerTag: v2.13.1
```

Now say that, depending on your build/deploy procedure, you want to bump the version number.

Create these three files:
```yaml
# bump-advisorui-docker-major.yaml
advisorUi:
  image:
    dockerTag: !ForceSemanticVer
      bump: major
```
```yaml
# bump-advisorui-docker-minor.yaml
advisorUi:
  image:
    dockerTag: !ForceSemanticVer
      bump: minor
```
```yaml
# bump-advisorui-docker-tiny.yaml
advisorUi:
  image:
    dockerTag: !ForceSemanticVer
      bump: tiny
```

Now in your build process you can bump different versions by passing the particular map file:
```bash
$ ./bump-version-yaml.sh advisorUi.yaml bump-advisorui-docker-major.yaml
```

## Example?

1. Get a YAML file, and put some version numbers as values in it. (see [example.yaml](example.yaml))

2. Make a duplicate of the YAML file's structure that leads to each version number. Where the version number would be, use a tag that references a kind of version. (see [map.yaml](map.yaml))

3. Run `make` at least once to generate a virtualenv environment.

4. Run `./bump-version-yaml.sh example.yaml map.yaml` (but, you know, substitute with your own files).

The example.yaml file should now have its version numbers bumped.

## Testing

Run `make test`.
