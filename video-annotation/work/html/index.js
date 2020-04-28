(function ($) {
	 var opts,isDown = false,index;	 
	$.fn.extend({
		
	  	slide: function(options){
 			var defaults = {
                ratio: '100', //Max value
                value: '', //default value，when range is true, value should be a n array
                range: false, //Not using two-way slider
				clickBack: function(){
					
				}
			  };

	  		opts = $.extend(defaults, options);
	  		return this.each(function(){
	  			var html,obj = $(this);
                if(opts.range){//decide using two-way slider
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
															
                }else{// one-way slider
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
                obj.html(html)
                obj.attr('data-ratio', opts.ratio);
                obj.attr('data-range', opts.range);
                fn.setValue(obj, opts)
                fn.action(obj, opts)
	  		})
	  	}
	})
    $('html,body').on('mouseup',function(){
		isDown = false
	})


	var fn = {
		action: function(obj, opts){
            if(this.browserRedirect()){
				obj.on('mousedown', '.chunk-one,.chunk-two', function(){
					isDown = true
					index = $(this).attr('data-index')
					$(this).css('z-index','20').siblings('span').css('z-index','5');
				})	
				obj.on('mousemove', function(event){
                    if(isDown){
                        var x = event.clientX-obj.find(".range")[0].offsetLeft;
						if(x > obj.find(".range").width()){
							x = obj.find(".range").width()
						}else if(x<0){
							x=0
						}
                        opts.ratio = obj.attr('data-ratio');
                        opts.range = obj.attr('data-range');
                        fn.calculate(x, obj, opts)
					}
				})
            }else{
				obj.on('touchmove', '.chunk-one,.chunk-two' , function(event){
					$(this).css('z-index','20').siblings('span').css('z-index','5');
					index = $(this).attr('data-index')
                    var x = event.originalEvent.touches[0].clientX-obj.find(".range")[0].offsetLeft;
					if(x > obj.find(".range").width()){
						x = obj.find(".range").width()
					}else if(x<0){
						x=0
					}
                    fn.calculate(x, obj, opts)
				})
			}
		},
	 	//计算滑块值	
	 	calculate: function(x, obj, opts){
            if(opts.range === 'true' || opts.range == true){
	 			var one = obj.find('.chunk-one'),two = obj.find('.chunk-two');
				var oneLeft = one.position().left,twoLeft = two.position().left,width = obj.find(".range").width()
                if(index == 1){
                    if( x >= twoLeft){
						return false
					}

					var textN = x*(opts.ratio/100)
					one.find('strong').text(Math.round(textN/width*100))

					var num = (Math.round(x/width*opts.ratio)*100)/opts.ratio
					one.css('left', num+"%")					
				}else if(index == 2){
                    if(oneLeft >= x){
						return false
					}

					var textN = x*(opts.ratio/100)
					two.find('strong').text(Math.round(textN/width*100))

					var num = (Math.round(x/width*opts.ratio)*100)/opts.ratio
					two.css('left', num+"%")	
				}

				obj.find('.strip-two').css({'left': one.position().left+'px','width': (two.position().left-one.position().left)+'px'})
				setTimeout(function(){

					obj.find('.strip-two').css({'left': one.position().left+'px','width': (two.position().left-one.position().left)+'px'})
				},300)

				opts.clickBack([one.find('strong').text(), two.find('strong').text()])
            }else {
	 			var two = obj.find('.chunk-two'),width = obj.find(".range").width()

				var textN = x*(opts.ratio/100)
				two.find('strong').text(Math.round(textN/width*100))

				var num = (Math.round(x/width*opts.ratio)*100)/opts.ratio
				two.css('left', num+"%")					


				obj.find('.strip-two').css({'width': (two.position().left)+'px'})
				setTimeout(function(){

					obj.find('.strip-two').css({'width': (two.position().left)+'px'})
				},300)

				opts.clickBack([two.find('strong').text()])
	 		}
	 	},

	 	setValue: function(self, options){
            if(options.range){
  				var one = self.find('.chunk-one'),two = self.find('.chunk-two');
  				options.value == '' ? options.value = ['0', options.ratio] : options.value 

  				self.find('.chunk-one').css('left', Math.round(options.value[0]/options.ratio*100)+'%')
	  			self.find('.chunk-two').css('left', Math.round(options.value[1]/options.ratio*100)+'%')

	  			self.find('.chunk-one strong').text(options.value[0])
	  			self.find('.chunk-two strong').text(options.value[1])

	  			self.find('.strip-two').css({'left': one.position().left+'px','width': (two.position().left-one.position().left)+'px'})
  			}else{//单滑块
  				var two = self.find('.chunk-two');
  				options.value == '' ? options.value = [options.ratio/2] : options.value 
				if(typeof options.value == 'string'){

	  				two.css('left', Math.round(options.value/options.ratio*100)+'%')	

	  				self.find('.chunk-two strong').text(options.value)
				}else{

	  				two.css('left', Math.round(options.value[0]/options.ratio*100)+'%')	

	  				self.find('.chunk-two strong').text(options.value[0])
				}

				self.find('.strip-two').css({'width': (two.position().left)+'px'})
  			}
  		},

        //check the user device type
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

