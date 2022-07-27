# n64RomConversion

This is a simple python script for converting between Nintendo 64 Rom file types (n64, v64, z64) with **zero dependencies** (other than Python 3.10+). This was a fairly simple exercise as all n64 file types are just slightly obfuscated versions of each other. I would highly recommend reading the links in [Credits](#Credits) and program it yourself.

I believe there was a Java version on Github a while ago but I can no longer find the repository. This should accomplish the same thing, except written in a more convenient language. More importantly, one that supports the [XDG Base Directory Specifications](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html). Non Linux users can feel free to ignore this.


## Running
```bash
python main.py -i baserom.{n64|z64|v64} -o output.{n64,z64,v64}
```

### Examples
```bash
python main.py -i baserom.n64 -o output.z64
python main.py -i output.z64 -o other.v64
```


# Credits

* [Wikipedia's Article on n64 rom file formats](https://en.wikipedia.org/wiki/List_of_Nintendo_64_ROM_file_formats)
  * A nice preamble for the uninformed
* [A nice thread explaining the technical differences between file types](https://jul.rustedlogic.net/thread.php?id=11769)
  * A nice read if you wish to program the conversion yourself
