(function ($) {
	/**
	 * 2018-9-20 星期四
	 * //默认参数 (放在插件外面，避免每次调用插件都调用一次，节省内存)
	 * =============================================================
	 * 由于放在此处会造成缓存，影响下次插件使用 （已放下面插件中）
	 * 
	  var defaults = {
	    ratio: '100', //滑动最大值
	    value: '', //默认值，range为true时 此时绑定值是一个数组
	    range: false,//是否开启双向滑动
		clickBack: function(){
			
		}
	  };
	  */
	 //设置全局变量
	 var opts,isDown = false,index;	 
	//扩展方法
	$.fn.extend({
		
	  	slide: function(options){
	  		 //默认参数 
 			var defaults = {
			    ratio: '100', //滑动最大值
			    value: '', //默认值，range为true时 此时绑定值必须是一个数组
			    range: false,//是否开启双向滑动
				clickBack: function(){
					
				}
			  };
	  		//扩展对象，覆盖默认对象
	  		opts = $.extend(defaults, options);
	  		return this.each(function(){
	  			var html,obj = $(this);
	  			if(opts.range){//判断是否开启双向滑动
					html = '<div class="range">'+
							'<span class="chunk-one" data-index="1">'+
								'<strong>0</strong>'+
							'</span>'+
							'<span class="chunk-two" data-index="2">'+
								'<strong>'+opts.ratio+'</strong>'+
							'</span>'+
							'<div class="strip-one">'+
								
							'</div>'+
							'<div class="strip-two">'+
								
							'</div>'+
						'</div>';
															
				}else{//单滑块
					html = '<div class="range">'+
								'<span class="chunk-two" data-index="2">'+
									'<strong>'+opts.ratio+'</strong>'+
								'</span>'+
								'<div class="strip-one">'+
									
								'</div>'+
								'<div class="strip-two">'+
									
								'</div>'+
							'</div>';
							
				}
				obj.html(html)//添加html
				obj.attr('data-ratio', opts.ratio);//设置最大值，用于后面组件取值
				obj.attr('data-range', opts.range);//设置滑块类型，用于后面组件取值
				fn.setValue(obj, opts)//设置默认值
				fn.action(obj, opts)//事件操作
	  		})
	  	}
	})
	$('html,body').on('mouseup',function(){//鼠标松开
		isDown = false
	})
	//全局方法
	var fn = {
		action: function(obj, opts){
			if(this.browserRedirect()){//判断设备  pc端使用mouse事件
				obj.on('mousedown', '.chunk-one,.chunk-two', function(){
					isDown = true
					index = $(this).attr('data-index')
					$(this).css('z-index','20').siblings('span').css('z-index','5');
				})	
				obj.on('mousemove', function(event){
					if(isDown){//鼠标按下时滑动生效
						var x = event.clientX-obj.find(".range")[0].offsetLeft;//获取滑动的X轴
						if(x > obj.find(".range").width()){
							x = obj.find(".range").width()
						}else if(x<0){
							x=0
						}
						opts.ratio = obj.attr('data-ratio');//获取当前组件的最大值
						opts.range = obj.attr('data-range');//获取当前组件的滑块类型
						fn.calculate(x, obj, opts) //计算滑块值		
					}
				})
			}else{//移动端使用touch事件
				obj.on('touchmove', '.chunk-one,.chunk-two' , function(event){
					$(this).css('z-index','20').siblings('span').css('z-index','5');
					index = $(this).attr('data-index')
					var x = event.originalEvent.touches[0].clientX-obj.find(".range")[0].offsetLeft;//获取滑动的X轴
					if(x > obj.find(".range").width()){
						x = obj.find(".range").width()
					}else if(x<0){
						x=0
					}
					fn.calculate(x, obj, opts) //计算滑块值		
				})
			}
		},
	 	//计算滑块值	
	 	calculate: function(x, obj, opts){
	 		if(opts.range == 'true' || opts.range == true){//判断是否开启双向滑动
	 			var one = obj.find('.chunk-one'),two = obj.find('.chunk-two');
				var oneLeft = one.position().left,twoLeft = two.position().left,width = obj.find(".range").width()
				if(index == 1){//第一个滑块滑动时	
					if( x >= twoLeft){//第一个滑块不能大于第二个
						return false
					}
					//计算数值
					var textN = x*(opts.ratio/100)
					one.find('strong').text(Math.round(textN/width*100))
					//计算滑动值
					var num = (Math.round(x/width*opts.ratio)*100)/opts.ratio
					one.css('left', num+"%")					
				}else if(index == 2){
					if(oneLeft >= x){//第一个滑块不能大于第二个
						return false
					}
					//计算数值
					var textN = x*(opts.ratio/100)
					two.find('strong').text(Math.round(textN/width*100))
					//计算滑动值
					var num = (Math.round(x/width*opts.ratio)*100)/opts.ratio
					two.css('left', num+"%")	
				}
				//设置选着范围宽度
				obj.find('.strip-two').css({'left': one.position().left+'px','width': (two.position().left-one.position().left)+'px'})
				setTimeout(function(){
					//由于使用动画，延时处理
					obj.find('.strip-two').css({'left': one.position().left+'px','width': (two.position().left-one.position().left)+'px'})
				},300)
				//回调数据	  		
				opts.clickBack([one.find('strong').text(), two.find('strong').text()])
	 		}else {//单滑块
	 			var two = obj.find('.chunk-two'),width = obj.find(".range").width()
				//计算数值
				var textN = x*(opts.ratio/100)
				two.find('strong').text(Math.round(textN/width*100))
				//计算滑动值
				var num = (Math.round(x/width*opts.ratio)*100)/opts.ratio
				two.css('left', num+"%")					

				//设置选着范围宽度
				obj.find('.strip-two').css({'width': (two.position().left)+'px'})
				setTimeout(function(){
					//由于使用动画，延时处理
					obj.find('.strip-two').css({'width': (two.position().left)+'px'})
				},300)
				//回调数据	  		
				opts.clickBack([two.find('strong').text()])
	 		}
	 	},
	 	//设置默认值
	 	setValue: function(self, options){
  			if(options.range){//双向滑块
  				var one = self.find('.chunk-one'),two = self.find('.chunk-two');
  				options.value == '' ? options.value = ['0', options.ratio] : options.value 
  				//设置偏移数
  				self.find('.chunk-one').css('left', Math.round(options.value[0]/options.ratio*100)+'%')
	  			self.find('.chunk-two').css('left', Math.round(options.value[1]/options.ratio*100)+'%')
	  			//设置数值
	  			self.find('.chunk-one strong').text(options.value[0])
	  			self.find('.chunk-two strong').text(options.value[1])
	  			//设置选着范围宽度
	  			self.find('.strip-two').css({'left': one.position().left+'px','width': (two.position().left-one.position().left)+'px'})
  			}else{//单滑块
  				var two = self.find('.chunk-two');
  				options.value == '' ? options.value = [options.ratio/2] : options.value 
				if(typeof options.value == 'string'){
					//设置偏移数
	  				two.css('left', Math.round(options.value/options.ratio*100)+'%')	
	  				//设置数值
	  				self.find('.chunk-two strong').text(options.value)
				}else{
					//设置偏移数
	  				two.css('left', Math.round(options.value[0]/options.ratio*100)+'%')	
	  				//设置数值
	  				self.find('.chunk-two strong').text(options.value[0])
				}
  				//设置选着范围宽度
				self.find('.strip-two').css({'width': (two.position().left)+'px'})
  			}
  		},
  		//判断设备
  		browserRedirect: function(){
  			var sUserAgent = navigator.userAgent.toLowerCase();
            var bIsIpad = sUserAgent.match(/ipad/i) == "ipad";
            var bIsIphoneOs = sUserAgent.match(/iphone os/i) == "iphone os";
            var bIsMidp = sUserAgent.match(/midp/i) == "midp";
            var bIsUc7 = sUserAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
            var bIsUc = sUserAgent.match(/ucweb/i) == "ucweb";
            var bIsAndroid = sUserAgent.match(/android/i) == "android";
            var bIsCE = sUserAgent.match(/windows ce/i) == "windows ce";
            var bIsWM = sUserAgent.match(/windows mobile/i) == "windows mobile";
            if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) {
                return false
            } else {
                return true
            }
  		}
	 }
})(jQuery)

