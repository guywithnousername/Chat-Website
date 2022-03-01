const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: 'phaser-game',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 110 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};
const game = new Phaser.Game(config);
let player;
let sword;
let mx;
let my;
let jab;
const centerx = game.config.width / 2;
const centery = game.config.height / 2;
const w = game.config.width;
const h = game.config.height;
const pointer = game.input.activePointer;
function preload() {
	this.load.image('sky','static/assets/sky.png');
	this.load.image('sword','static/assets/sword.png');
	this.load.image('cube','static/assets/cube.png');
	this.load.image('ground','static/assets/ground.png');
}
function create() {
	background = this.add.image(centerx,centery,'sky');
	background.displayWidth=w;
	background.displayHeight=h;

	sword = this.physics.add.sprite(centerx,centery,'sword').setImmovable(true);
	sword.body.setAllowGravity(false);
	sword.displayWidth = w / 20;
	sword.displayHeight = (w / 20) * (229/97); //sword dimensions: 97 to 229
	sword.setBodySize(97, 229)

	cube = this.physics.add.sprite(centerx,centery,'cube');
	cube.displayWidth = w / 15;
	cube.displayHeight = w / 15;
	cube.setBodySize(w / 20, w / 20)

	ground = this.physics.add.staticGroup();
	let g = ground.create(0, h - h / 10,'ground').setOrigin(0,0);
	console.log("create", h, h - h/10)
	console.log("oldg ", g)
	g.displayWidth = w;
	g.displayHeight = h / 10;
	g.setBodySize(g.displayWidth, g.displayHeight, true);
	g.setOffset(240, 30)
	this.physics.add.collider(cube, ground);
}
function update() {
	// START sword code
	if (pointer.isDown) {
		jab = 110;
	} else {
		jab = 90;
	}

	mx = game.input.mousePointer.x - cube.x;
	my = game.input.mousePointer.y - cube.y;
	let hyp = Math.sqrt(mx * mx + my * my);

	sword.x = (jab * mx) / hyp + cube.x;
	sword.y = (jab * my) / hyp + cube.y;
	let an = Phaser.Math.Angle.Between(sword.x,sword.y,game.input.mousePointer.x,game.input.mousePointer.y);
	let ang = an * Phaser.Math.RAD_TO_DEG + 90;
	sword.angle = ang;
	// END sword code
	// START cube code
	
}
