# A Smoothed Fast–Slow Divergence Does Not Warn of Loss Spikes Earlier Than Deployed Alarms: A Pre-Registered Null on a Public 7B Training Log — the plain-English companion

*Companion to the research paper of the same title. This is education, not investment advice. Nothing here tells you what to buy, sell, or predict. It explains what the paper found, how the checking worked, and what the results do and do not mean.*

## The claim in one sentence

A smarter-looking early-warning alarm for AI training crashes, raced fairly against simple alarms, never warned earlier.

## Teaching a computer, and the hiccups that cost a fortune

Big AI models learn by practice. The computer reads some text and guesses the next word. It gets a score for how wrong it was, called the **loss**, and then nudges millions of internal settings to do a little better next time. That is one **step**. A large model takes hundreds of thousands of steps, over weeks, on thousands of chips.

Most of the time the loss drifts slowly downward, like a student's mistakes shrinking over a school year. Sometimes it suddenly jumps up. That jump is a **loss spike**. A bad spike can wreck the run, so engineers often rewind to a saved copy from earlier and skip the data that caused trouble. Rewinding throws away days of work on very expensive machines.

So people want an early warning. If something could beep a little before a spike, engineers could act sooner.

## The thing we watched: how hard the model is being shoved

At every step, the training program measures how big a nudge it is about to give the model's settings. That size is called the **gradient norm**. Think of it as how hard the steering wheel is being jerked. Calm driving means small jerks. Trouble often shows up as a sudden hard jerk.

Engineers who studied big runs noticed that the steering wheel often jerks hard just before the loss spikes. That is why every alarm in this study watches the gradient norm.

## Two kinds of smoke detector

The alarms people already use work like a jumpy smoke detector. Each one compares the newest reading with a recent average, and beeps if the newest one sticks out. In the paper's language, each is a "fast versus slow" comparison where the fast side is just one reading.

The idea we tested was gentler.
- Instead of the single newest reading, take the **average of the last 32 readings**. That is the "fast" average.
- Compare it with the **average of the last 128 readings**. That is the "slow" average.
- The gap between them is called the **divergence**.

Here is an everyday picture. Your report card has this month's average and this year's average. One bad quiz barely moves either one. But if your monthly average pulls clearly away from your yearly average, something real is changing. The hope was that this smoothed gap, called **D_div** in the paper, would notice trouble building up and beep earlier than the jumpy one-reading alarms.

D_div turns the gap into a score by ranking each new value against every earlier one. It is like asking whether today's gap is one of the biggest ever seen. It beeps when the rank passes a set bar, called its **trigger**. Setting the trigger higher means fewer beeps.

## A fair race needs equal false alarms

Comparing alarms is trickier than it sounds. A car alarm that goes off every time a truck drives past will "warn" you about every break-in, and also about a thousand trucks. Warning early means nothing if the alarm cries wolf all the time.

So every alarm was tuned to make the same number of false alarms: one false alarm per 10,000 readings taken away from any spike. Only then did we ask which alarm warned earliest before real spikes. The **lead** is how long before a spike an alarm first beeped. A miss counts as zero.

## Calling the shot before taking it

In pool, a player who calls "eight ball, corner pocket" before shooting gets credit only if that exact thing happens. Calling the shot stops anyone from claiming afterward that whatever happened was the plan.

This study did the same, called **pre-registration**. Before any of the real data were scored, the full plan was written down and published with a date on it. That included the alarms, the tuning, how a spike is defined, and a **kill rule**. The kill rule said: if the smoothed alarm's average lead is not bigger than the best simple alarm's, the project stops, the failure becomes the paper, and the bigger follow-up experiment is never run.

## The race

The data came from the public training diary of OLMo, a 7-billion-setting language model whose team publishes its logs. The diary records the loss at every step, but the gradient norm only every 10 steps. So all the alarms had to work with a snapshot every 10 steps, like a security camera that takes one photo every ten seconds.

A rule written in advance found the spikes in the loss: 57 of them were usable. Then the five alarms raced, once, on 15 November 2026.

## What happened

The smoothed alarm never got off the starting line. To keep its false alarms down to the allowed budget, its trigger had to be set impossibly high, so high that it never beeped at all. Picture a smoke detector so jumpy that the only way to stop it from going off while you cook is to unplug it. The paper's number for its trigger is ∞, meaning infinite.

The simple alarms did run, and they did no better. Not one of them beeped early before any of the 57 spikes. A few beeped at the very moment a spike was recorded: 2, 2 and 3 times for three of them. That is no use as a warning. Every alarm's average lead was 0 steps.

So the smoothed alarm did not beat the best simple alarm. Under the rule written down in advance, the result is **REFUTE**, the word the plan reserved for "the new idea lost". The project stopped.

When the alarms were allowed more false alarms, the simple ones started to catch a few spikes early. At five false alarms per 10,000 readings, the smoothed alarm finally switched on and caught some too. Even there, its average lead of 19 steps was behind the best simple alarm's 27. Most spikes were still missed by everyone.

## Why "nothing warned" does not mean "there was nothing to warn about"

It would be easy to read this as "spikes come with no warning." The study was built to stop that misreading.

Before the real race, the alarms were tested on thousands of fake training runs built by computer. Some fakes had no warning signs at all. Others had warning signs planted on purpose, so the right answer was known.

On fakes shaped like the real run, with no warning signs, the kill rule still said "smoothed alarm loses" 87% of the time. That is because when nothing warns, every alarm ties at zero, and a tie counts as a loss for the new idea. Even with a planted warning, it often said "loses."

So this result is fair evidence about one thing: the smoothed alarm did not beat the simple ones here. It is weak evidence about whether warning signs exist.

## A clue left behind

After the verdict, we ran a few extra checks that were planned in advance but are clearly labelled **exploratory**. That means they are clues, not proof.

The clue is about timing. On average, the gradient norm does rise before a spike, and the rise is bigger than at random moments. A measure of how easily that could be a fluke gives 0.014; smaller means less likely to be luck. But nearly all of the rise happens in the very last 10-step snapshot before the spike.

Think of a pot of milk boiling over, filmed by a camera that takes one photo every ten seconds. The milk sits calm in photo after photo, then foams over between two frames. An alarm that averages the last 32 photos barely moves when only the last photo changes. In this run, smoothing threw away the only signal there was.

A second clue: the smoothed alarm could not be tuned on any piece of the run, not on any one stretch, and not on either half of the longest stretch. That points to a problem with the alarm's design, not just bad luck with the data.

## What the checking caught in this paper

- **Overlapping comparison samples.** One extra check compared the 57 spikes against a large set of random moments. Many of those random moments overlapped each other heavily, which made the result look more certain than it was. The comparison was redone with non-overlapping moments. The fluke measure moved from "almost certainly not luck" to 0.014. The clue survived, but weaker, and the paper reports only the corrected number.
- **Missing context numbers.** The plan required some numbers to be printed beside the verdict, such as how often the rule says "loses" on fakes with no warning signs. They had been computed, but were missing from the paper's master list of numbers. They were added, without recomputing anything.
- **A gap in the data.** Part of the training run, roughly steps 14,000 to 52,000 and the very end, could not be used. Every result in the paper is stated as true for the covered part only.
- **A setting that differed from one rule text.** One random-number setting used in the race differed from one of the written rules. It could not change the verdict, because the verdict did not use random numbers, and the paper says so.

The records of these checks, and every independent review, are in the project's public repository, in its `verification/` folder and decision log.

## What this cannot do

- It is one training run, logged every 10 steps. A run logged at every step might give the smoothed alarm the detail it needs. This study cannot say.
- It covers only the usable part of that run.
- It does not show that spikes come without warning. It shows only that this alarm did not beat simple ones here.
- It does not test ways to prevent spikes, only ways to warn of them.
- The smoothed alarm is not offered as a tool. It lost, so it is not packaged for anyone to install.

How could this be wrong? Someone could run the same plan on a public training log that records the gradient norm at every step. If the smoothed alarm clearly led there, that would show the result here belongs to the 10-step snapshots, not to the idea itself. The prediction this study made in advance is already settled: the kill rule fired, as written.

## The takeaway

A careful test showed that smoothing a warning signal did not make it warn earlier about AI training crashes. On this run, the warning sign, if there is one, arrives too late and too suddenly for any alarm to use, at least when the measurements come only every ten steps. The plan was fixed before the data were scored, the result was reported as planned, and the project stopped where it said it would.

*This companion is licensed CC BY-NC 4.0. The research paper it accompanies is licensed CC BY-NC-ND 4.0, and the analysis and verification code is MIT-licensed. Education, not advice: nothing in this document is financial advice, an investment recommendation, or a forecast.*
