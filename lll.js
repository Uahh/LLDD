let MyHeader = {
	template: `<div id="header">我是头部</div>`,
};

let MyNav = {
	template: 
		`<div id="nav">
			我是导航栏<br/>
			<button @click="changeShow">点我显示数据</button>
			<ul v-if="dataShow">
				<li v-for="(item, index) in data">{{index}}、{{item.name}} ：{{item.age}}</li>
			</ul>
		</div>`,
	data() {
		return {dataShow: false};
	},
	methods: {
		changeShow() {
			this.dataShow = !this.dataShow;
		}
	},
	props: ['data'],
};

let MyMain = {
	template: `<div id="main">我是正文</div>`,
};

let MyBody = {
	components: {
		'my-nav': MyNav,
		'my-main': MyMain,
	},
	template: 
		`<div id="body">
			<my-nav :data="data"></my-nav>
			<my-main></my-main>
		</div>`,
	props: ['data'],
};

let MyFooter = {
	template: `<div id="footer">我是底部</div>`,
};

let App = {
	components: {
		'my-header': MyHeader,
		'my-body': MyBody,
		'my-footer': MyFooter,
	},
	template: 
		`<div>
			<my-header></my-header>
			<my-body :data="data"></my-body>
			<my-footer></my-footer>
		</div>`,
	props: ['data'],
};

let vm = new Vue({
	el: document.getElementById('app'),
	components: {
		'app': App,
	},
	template: '<app :data="data"/>',
	data() {
		return {
			data: [{name: 'bty', age: 12}, {name: '张三', age: 13}, {name: 'oppen', age: 14}]
		};
	}
});
