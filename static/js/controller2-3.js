var mulist = ["audio/Jam_July.mp3", "audio/BIGBANG - Blue [mqms2].flac", "audio/Queen - We Will Rock You [mqms2].flac"];
var muName = ["Jam_July", "BIGBANG - Blue", "Queen - We Will Rock You "];
console.log(mulist);
var name = document.getElementById("mutitle");
var i = 0;
function play(){
	var canvas = document.getElementById("target");

	var mu = document.getElementById("mu");
	console.log("获取播放器" + mu);
	var $mu_play;
	$mu_play = document.getElementById("play");
	
	if(mu.paused){
		console.log("播放" + $mu_play);

		mu.play();
		
	} else {
		console.log("停止" + $mu_play);
		mu.pause();
	}
}

function nextMu(){
	var mu = document.getElementById("mu");
	console.log("获取播放器" + mu);
	var $mu_next;
	$mu_next = document.getElementById("next");
	console.log("播放" + $mu_next);
	i++;
	if(i == mulist.length){
		i = 0;
	} 
	mu.src = mulist[i];
	name.text = muName[i];
	mu.play();
}

function lastMu(){
	var mu = document.getElementById("mu");
	var $mu_last;
	$mu_last = document.getElementById("last");
	console.log("播放" + $mu_last);
	i--;
	if(i == 0){
		i = mulist.length-1;
	} 
	mu.src = mulist[i];
	name.text = muName[i];
	mu.play();
}

function register(){
	var account;
	account = document.getElementById("account");
	var password;
	password = document.getElementById("password");
	var password2;
	password2 = document.getElementById("password2");

	if(password2 === password){
		
	} else {
		console.log("两次密码不对");
	}
}

function login(){
	
}

var stage = new createjs.Stage("mycanvas")
	createjs.Ticker.addEventListener("tick", stageBreakHandler);
	var img =  new Image()
	img.src = "img/horse.png"
	img.onload = function(){
		var ss = new createjs.SpriteSheet({
			"images": ["img/horse.png"], 
			"frames": [
				[519,1352,468,225,0,-39.5,-6.05],
				[525,694,405,225,0,-39.5,-6.05],
				[402,1577,398,241,0,-37.5,-9.05],
				[0,1565,402,239,0,-33.5,-8.05],
				[521,920,430,233,0,-23.5,-14.05],
				[520,0,465,228,0,-7.5,-22.05],
				[515,238,479,228,0,-8.5,-24.05],
				[508,470,500,224,0,-2.5,-26.05],
				[0,470,508,231,0,-5.5,-20.05],
				[0,238,515,232,0,-9.5,-17.05],
				[0,0,520,238,0,-12.5,-11.05],
				[0,920,521,219,0,-18.5,-11.05],
				[0,701,525,219,0,-18.5,-11.05],
				[0,1352,519,213,0,-28.5,-10.05],
				[0,1139,520,213,0,-28.5,-10.05]
			],
			"animations" : {
				"run": [0,14,"run"]
			}
		})
	
		var sp = new createjs.Sprite(ss,"run")
		stage.addChild(sp)
		stage.update();
	}
	
	function stageBreakHandler(event){
		stage.update();
	}