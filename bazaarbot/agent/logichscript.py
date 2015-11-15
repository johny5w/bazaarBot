#! /usr/bin/env python

from market import *
from agent import *


class LogicHScript(Logic)
{
	var script:String = "";
	var source:String;
	
	public function new(?data:Dynamic) 
	{
		super(data);
		if (data == null) return;
		if (Std.is(data, String))
		{
			script = Assets.getText("assets/scripts/"+data);
		}
	}
	
	override public function perform(agent:Agent, bazaar:Market):Void 
	{
		_perform_script(script, agent, bazaar);
	}
	
	private function _perform_script(script:String, agent:Agent, bazaar:Market):Void
	{
		var parser = new Parser();
		var ast = parser.parseString(script);
		var interp = new Interp();
		
		var vars:Map<String,Dynamic> = 
		[
		 "agent" => agent, 
		 "query_inventory" => agent.queryInventory,
		 "produce" => _produce,
		 "consume" => _consume,
		 "inventory_is_full" => agent.get_inventoryFull,
		 "make_room_for" => 
			function(a:Agent, c:String = "food", amt:Float = 1.0):Void
			{ 
				var to_drop:String = bazaar.getCheapestCommodity(10, [c]);
				if (to_drop != "") {_consume(a, to_drop, amt);}
			}
		 ];
		 
		interp.variables = vars;
		interp.execute(ast);
	}
}
