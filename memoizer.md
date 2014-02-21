    //JavaScript : The Good Parts
    //闭包，存储数据
    var memoizer = function (memo, formula) {
    	var recur = function(n){
    		var result = memo[n];
    		if (typeof result !== 'number') {
    			result = formula(recur, n);
    			memo[n] = result;
    		};
    		return result;
    	}
    	return recur;
    };
    //费波纳契数列
    var fibonacci = memoizer([0,1], function(recur, n){
    	return recur(n - 1) + recur(n -2);
    });
    //阶乘
    var factorial = memoizer([1,1], function(recur, n){
    	return n * recur(n - 1);
    });
    
    

    //Python 装饰器
    //http://programmingbits.pythonblogs.com/27_programmingbits/archive/50_function_decorators.html
    def memoize(f):
    cache = {}
    def helper(x):
        if x not in cache:            
            cache[x] = f(x)
        return cache[x]
    return helper
    
    
    @memoize
    def fib(n):
        if n in (0, 1):
            return n
        else:
            return fib(n - 1) + fib(n - 2)
