// This is supposed to add confetti whenever the user does something they
// did not do before, but I don't know how to run Javascript from Python.



const jsConfetti = new JSConfetti()

jsConfetti.addConfetti({
    confettiRadius: 6,
    confettiNumber: 500,
})
function confetti() {
    jsConfetti.addConfetti()
}
