const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: 'phaser-game',
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
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
let punch = 1;
function preload() {
	this.load.image('player','static/assets/player.png');
	this.load.image('punchleft','static/assets/playerleft.png');
	this.load.image('punchright','static/assets/playerright.png');
}
function create() {
	player = this.physics.add.sprite(400,300,'player');
}
function ppunch() {
    if (punch === 1) {
	player.setTexture('punchleft');
        punch = 0;
    } else {
	player.setTexture('punchright');
        punch = 1;
    }
}
function update() {
	ppunch()
}
