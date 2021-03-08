% rebase('layout.tpl', title=title, year=year)

<div class="jumbotron">
	<h3>{{ title }}</h3>
	<h4>{{ message }}</h4>

	<p>为了方便开发者在移动端进行服务器的搭建和查看，这个项目使用了简易的PyWeb开发框架Bottle，并且通过Android端的QPython编译器，对该项目进行编译运行。</p>
	<div class="row">
	    <div class="col-md-4">
	        <h3>Python拓展库</h3>
	        <p>PyPI中有Python各种拓展库，通过PyPI的使用，对服务器实现其他各种功能，例如：数据库等</p>
	        <p><a class= "btn btn-default"
	        href="https://pypi.python.org/pypi">Learn more &raquo;</a></p>
	    </div>
	    <div class="col-md-4">
	    	<h3>Bottle教程</h3>
			<p>Bottle是一个简易的PyWeb框架，除了Python标准库之外，不再依赖其他的Python拓展库，是在Android平台中实现服务器的一个比较便利的Web框架</p>
			<p><a class= "btn btn-default"
	        href="(http://www.bottlepy.org/docs/dev/index.html">Learn more &raquo;</a></p>
	    </div>
	    <div class="col-md-4">
	        <h2>QPython</h2>
	        <p>QPython是Android系统中的一个Python编译器，可以运行简易的Python项目，通过这一个工具，来运行这个简易PyWeb项目，使其可以在Android中运行</p>
	        <p><a class="btn btn-default" href="https://github.com/qpython-android/qpython">Learn more &raquo;</a></p>
	    </div>
	</div>
</div>