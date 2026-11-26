import sys
COMMON = ".u{display:none}.s1{opacity:.82}.s2{opacity:.62}.s3{opacity:.42}"
EXTRA = {
  "dark": ":root{--ce:#121722;--cb:#0000}.s{filter:drop-shadow(0 0 5px #5c74ff) drop-shadow(0 0 12px #3d5cff)}"
          ".c:not([class='c']){filter:drop-shadow(0 0 3px #3d5cff99)}",
  "light": ".s{filter:drop-shadow(0 2px 4px #1d3bff55)}",
}
path, mode = sys.argv[1], sys.argv[2]
s = open(path).read()
s = s.replace("</style>", COMMON + EXTRA[mode] + "</style>", 1)
open(path, "w").write(s)
