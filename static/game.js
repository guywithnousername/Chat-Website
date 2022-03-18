const config = {
    type: Phaser.AUTO,
    width: 480,
    height: 480,
    backgroundColor: "#497f3f",
    parent: 'phaser-game',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: true
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};
const game = new Phaser.Game(config);

function preload() {
	this.load.image('soil','/static/assets/tilesets/plowed_soil.png');
	this.load.image('fences','/static/assets/tilesets/fence.png');
	this.load.image('sand','/static/assets/tilesets/sand.png');
	this.load.tilemapTiledJSON('map', '/static/assets/farm.json');
}
function create() {
	map = this.make.tilemap({ key: 'map' });
	
	let sand = map.addTilesetImage('sand','sand');
	let sandlayer = map.createLayer('Sand',sand, 0, 0);
	let soil = map.addTilesetImage('plowed_soil','soil');
	let soillayer = map.createLayer('Soil',soil,0,0);
	let fences = map.addTilesetImage('fences','fences');
	let fencelayer = map.createLayer('Fences',fences,0,0);

	map.setCollisionByExclusion(-1,true,fencelayer);
}
function update() {

}
