'use client';
import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
  const [runningCount, setRunningCount] = useState(0);
  const [trueCount, setTrueCount] = useState(0);
  const [decks, setDecks] = useState(8);
  const [cards, setCards] = useState(0);
  const [aces, setAces] = useState(0);
  const [cardsLeft, setCardsLeft] = useState(0);
  const [decksLeft, setDecksLeft] = useState(0);

  function calculateDecks(decks: number) {
    setDecks(decks)
    setCards(decks * 52)
    setAces(decks * 4)
    setCardsLeft(decks * 52)
    setDecksLeft(decks)
  }

  function reset() {
    calculateDecks(decks)
    setRunningCount(0)
    setTrueCount(0)
  }

  function addCard(value: number) {
    setCardsLeft(cardsLeft - 1)
    setDecksLeft(cardsLeft / 52)
    setRunningCount(runningCount + value)
    setTrueCount((runningCount + value) / (cardsLeft / 52))
  }

  useEffect(() => {
    const keyDownHandler = (e: any) => {
      console.log(`You pressed ${e.code}.`);
      if (e.code == "KeyZ") {
        addCard(1)
      }
      if (e.code == "KeyX") {
        addCard(0)
      }
      if (e.code == "KeyC") {
        addCard(-1)
      }
    }
    document.addEventListener("keydown", keyDownHandler);
    // clean up
    return () => {
      document.removeEventListener("keydown", keyDownHandler);
    };
  }, [cardsLeft, runningCount, decksLeft]);

  // <2 = 1 unit
  // +2 = 2 units
  // +3 = 4 units
  // +4 = 8 units
  // Omega II
  // Wong Halves


  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-4">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <div className="flex flex-col">
          <div className="flex-row items-center justify-between">
            <div className="flex items-center">
              <label htmlFor="decks" className="mr-4">Decks</label>
              <input
                className="text-black"
                type="number"
                id="decks"
                name="decks"
                min="1"
                max="8"
                value={decks}
                onChange={(e) => calculateDecks(parseInt(e.target.value))}
              />
            </div>
            <div className="flex items-center">
              <label htmlFor="cards" className="mr-4">Cards</label>
              <input
              className="text-black"
                type="number"
                id="cards"
                name="cards"
                min="0"
                max="1000"
                value={cards}
                onChange={(e) => setCards(parseInt(e.target.value))}
              />
            </div>
            <div className="flex items-center mt-4">
              <label htmlFor="aces" className="mr-4">Aces</label>
              <input
              className="text-black"
                type="number"
                id="aces"
                name="aces"
                min="0"
                max="32"
                value={aces}
                onChange={(e) => setAces(parseInt(e.target.value))}
              />
            </div>
          </div>
          <div className="flex-row items-center justify-between">
            <div className="flex items-center">
              <label htmlFor="cardsLeft" className="mr-4">Cards Left</label>
              <input
              className="text-black"
                type="number"
                id="cardsLeft"
                name="cardsLeft"
                min="0"
                max="1000"
                value={cardsLeft}
                onChange={(e) => setCardsLeft(parseInt(e.target.value))}
              />
            </div>
            <div className="flex items-center">
              <label htmlFor="decksLeft" className="mr-4">Decks Left</label>
              <input
              className="text-black"
              style={{ width: '50px' }}
                type="number"
                id="decksLeft"
                name="decksLeft"
                min="0"
                max="8"
                value={decksLeft}
                onChange={(e) => setDecksLeft(parseFloat(e.target.value))}
              />
            </div>
          </div>
          <div className="flex-row items-center justify-between mt-2">
            <div className="flex items-center">
              <label htmlFor="running count" className="mr-4">Running Count</label>
              <input
              className="text-black"
                type="number"
                id="running count"
                name="running count"
                min="-20"
                max="20"
                value={runningCount}
                onChange={(e) => setRunningCount(parseInt(e.target.value))}
              />
            </div>
            <div className="flex items-center">
              <label htmlFor="true count" className="mr-4">True Count</label>
              <input
              className="text-black"
                type="number"
                id="true count"
                name="true count"
                min="-20"
                max="20"
                value={trueCount}
                onChange={(e) => setTrueCount(parseFloat(e.target.value))}
              />
            </div>
            <div className="flex items-center mt-4">
              <input
                className="bg-indigo-500 text-white rounded-md px-4 py-1 hover:bg-indigo-600 active:bg-indigo-700"
                type="button"
                id="true count"
                value="2-6"
                onClick={(e) => {addCard(1)}}
              />
              <input
                className="bg-indigo-500 text-white rounded-md px-4 py-1 ml-2 hover:bg-indigo-600 active:bg-indigo-700"
                type="button"
                id="true count"
                value="7-9"
                onClick={(e) => {addCard(0)}}
              />
              <input
                className="bg-indigo-500 text-white rounded-md px-4 py-1 ml-2 hover:bg-indigo-600 active:bg-indigo-700"
                type="button"
                id="true count"
                value="10+"
                onClick={(e) => {addCard(-1)}}
              />
            </div>
            <div className="flex items-center mt-4 hover:bg-red-600 active:bg-red-700">
              <input
                className="bg-red-500 text-white rounded-md px-4 py-1"
                type="button"
                id="true count"
                value="RESET"
                onClick={(e) => reset()}
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
