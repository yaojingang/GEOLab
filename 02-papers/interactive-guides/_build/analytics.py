"""Keep the requested Baidu visitor statistics on generated learning pages."""

ANALYTICS_ID = "c0aa4d814a9bb0449f84d59c73cc5da4"
SCRIPT_URL = "https://hm.baidu.com/hm.js?" + ANALYTICS_ID
SNIPPET = '''<!-- Baidu visitor statistics -->
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?c0aa4d814a9bb0449f84d59c73cc5da4";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
'''


def with_baidu_analytics(document):
    count = document.count(SCRIPT_URL)
    if count > 1:
        raise ValueError("Duplicate Baidu analytics loaders")
    if count == 1:
        return document
    if document.count("</head>") != 1:
        raise ValueError("A single HTML head is required")
    return document.replace("</head>", SNIPPET + "</head>", 1)
